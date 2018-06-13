#!/usr/bin/env python3

""" This file contains some utilities used for processing data and 
    writing data to BigQuery.
"""

import os, time, logging, struct, sys, traceback
from datetime import datetime
from google.cloud import bigquery
from google.cloud import datastore
from google.cloud import storage


# should be enough retries to insert into BQ
NUM_RETRIES = 3


# keys common to all messages
messageType_KEY = 'messageType'
messageType_EnvVar = 'EnvVar'
messageType_CommandReply = 'CommandReply'
messageType_Image = 'Image'

# keys for messageType='EnvVar' (and also 'CommandReply')
var_KEY = 'var'
values_KEY = 'values'


#------------------------------------------------------------------------------
def validDictKey( d, key ):
    if key in d:
        return True
    else:
        return False


#------------------------------------------------------------------------------
# returns the messageType key if valid, else None.
def validateMessageType( valueDict ):

    if not validDictKey( valueDict, messageType_KEY ):
        logging.error('Missing key %s' % messageType_KEY )
        return None

    if messageType_EnvVar == valueDict[ messageType_KEY ]:
        return messageType_EnvVar

    if messageType_CommandReply == valueDict[ messageType_KEY ]:
        return messageType_CommandReply

    if messageType_Image == valueDict[ messageType_KEY ]:
        return messageType_Image

    logging.error('validateMessageType: Invalid value {} for key {}'.format(
        valueDict[ messageType_KEY ], messageType_KEY ))
    return None


#------------------------------------------------------------------------------
# Make a BQ row that matches the table schema for the 'vals' table.
# (python will pass only mutable objects (list) by reference)
def makeBQEnvVarRowList( valueDict, deviceId, rowsList, idKey ):
    # each received EnvVar type message must have these fields
    if not validDictKey( valueDict, var_KEY ) or \
       not validDictKey( valueDict, values_KEY ):
        logging.error('makeBQEnvVarRowList: Missing key(s) in dict.')
        return

    varName =   valueDict[ var_KEY ]
    values =    valueDict[ values_KEY ]

    # clean / scrub / check the values.  
    deviceId =  deviceId.replace( '~', '' ) 
    varName =   varName.replace( '~', '' ) 

    # NEW ID format:  <KEY>~<valName>~<created UTC TS>~<deviceId>
    ID = idKey + '~{}~{}~' + deviceId

    row = ( ID.format( varName, 
        time.strftime( '%Y-%m-%dT%H:%M:%SZ', time.gmtime() )), # id column
        values ) # values column (no X or Y)

    rowsList.append( row )


#------------------------------------------------------------------------------
# returns True if there are rows to insert into BQ, false otherwise.
def makeBQRowList( valueDict, deviceId, rowsList ):

    messageType = validateMessageType( valueDict )
    if None == messageType:
        return False

    # write envVars and images (as envVars)
    if messageType_EnvVar == messageType or \
       messageType_Image == messageType:
        makeBQEnvVarRowList( valueDict, deviceId, rowsList, 'Env' )
        return True

    if messageType_CommandReply == messageType:
        makeBQEnvVarRowList( valueDict, deviceId, rowsList, 'Cmd' )
        return True

    return False

"""
example of the MQTT device telemetry message we receive:

# a packed binary image which contains its name
data=b'pascal-string-length-prefixed-camera-name, then image binary'

# JSON string image env. var.
data=b'{"messageType": "Image", "var": "webcam-top","{'values':[{'name':'URL', 'type':'str', 'value':'https://storage.googleapis.com/openag-v1-images/EDU-E40B8A78-f4-0f-24-19-fe-88_webcam-top_2018-06-13T16%3A20%3A20Z.png'}]}" }'
  deviceId=EDU-B90F433E-f4-0f-24-19-fe-88
  subFolder=
  deviceNumId=2800007269922577

# JSON string command reply
data=b'{"messageType": "CommandReply", "var": "status", "values": "{\\"name\\":\\"rob\\"}"}'
  deviceId=EDU-B90F433E-f4-0f-24-19-fe-88
  subFolder=
  deviceNumId=2800007269922577
"""


#------------------------------------------------------------------------------
# Create a temp PNG file from the imageBytes.
# Copy the file to cloud storage.
# The cloud storage bucket we are using allows "allUsers" to read files.
# Return the public URL to the PNG file in a cloud storage bucket.
def saveFileInCloudStorage( CS, varName, imageBytes, deviceId, CS_BUCKET ):

    bucket = CS.bucket( CS_BUCKET )
    filename = '{}_{}_{}.png'.format( deviceId, varName,
        time.strftime( '%Y-%m-%dT%H:%M:%SZ', time.gmtime() ))
    blob = bucket.blob( filename )

    blob.upload_from_string( imageBytes, content_type='image/png' )
    logging.info( "saveFileInCloudStorage: image saved to %s" % \
            blob.public_url )
    return blob.public_url


#------------------------------------------------------------------------------
# Save the URL as an entity in the datastore, so the UI can fetch it.
def saveImageURLtoDatastore( DS, deviceId, publicURL, cameraName ):
    key = DS.key( 'Images' )
    image = datastore.Entity(key, exclude_from_indexes=[])
    image.update( {
        'device_uuid': deviceId,
        'URL': publicURL,
        'camera_name': cameraName,
        'creation_date': datetime.now()
        } )
    DS.put( image )  
    logging.debug( "saveImageURLtoDatastore: saved Images entity" )
    return 


#------------------------------------------------------------------------------
# Parse and save the image
def save_image( CS, DS, BQ, dataBlob, deviceId, PROJECT, DATASET, TABLE, 
        CS_BUCKET ):

    try:
        """ debugrob from jbrain image sending code:

            maxMessageSize = 250 * 1024
            imageSize = len( imageBytes )
            totalChunks = math.ceil( imageSize / maxMessageSize )
            imageStartIndex = 0
            imageEndIndex = imageSize
            if imageSize > maxMessageSize:
                imageEndIndex = maxMessageSize

            for chunk in range( 0, totalChunks ):
                chunkSize = 4 # 4 byte uint
                totalChunksSize = 4 # 4 byte uint
                nameSize = 101 # 1 byte for pascal string size, 100 chars.
                endNameIndex = chunkSize + totalChunksSize + nameSize
                packedFormatStr = 'II101p' # uint, uint, 101b pascal string.

                dataPacked = struct.pack( packedFormatStr, 
                    bytes( chunk, totalChunks, variableName, 'utf-8' )) 

                # make a mutable byte array of the image data
                imageBA = bytearray( imageBytes ) 
                imageChunk = bytes( imageBA[ imageStartIndex:imageEndIndex ] )

                ba = bytearray( dataPacked ) 
                # append the image after two ints and string
                ba[ endNameIndex:endNameIndex ] = imageBytes 
                bytes_to_publish = bytes( ba )

                # publish this chunk
                self.mqtt_client.publish( self.mqtt_topic, bytes_to_publish, 
                        qos=1)
                self.logger.info('publishBinaryImage: sent image chunk ' 
                        '{} of {} for {}'.format( 
                            chunk, totalChunks, variableName ))

                # for next chunk, start at the ending index
                imageStartIndex = imageEndIndex 
                imageEndIndex = imageSize # is this the last chunk?
                # if we have more than one chunk to go, send the max
                if imageSize - imageStartIndex > maxMessageSize:
                    imageEndIndex = maxMessageSize # no, so send max.
        """
#debugrob: on server put chunks into datastore MqttCache entities
# chunkNum of totalChunks.  
# For every message received, check data store to see if we can assemble chunks.
# Messages will probably be received out of order.

        # break the length prefixed name apart from the image data in the blob
        endNameIndex = 101 # 1 byte for pascal string size, 100 chars.
        ba = bytearray( dataBlob ) # need to use a mutable bytearray
        namePacked = bytes( ba[ 0:endNameIndex ] )# slice off first name chars
        namePackedFormatStr = '101p'
        unpackPascalStr = struct.unpack( namePackedFormatStr, namePacked )
        varName = unpackPascalStr[0].decode( 'utf-8' )
        imageBytes = bytes( ba[ endNameIndex: ] ) # rest of array is image data

        publicURL = saveFileInCloudStorage( CS, varName,
            imageBytes, deviceId, CS_BUCKET )
        
        saveImageURLtoDatastore( DS, deviceId, publicURL, varName )

        message_obj = {}
        message_obj['messageType'] = messageType_Image
        message_obj['var'] = varName
        valuesJson = "{'values':["
        valuesJson += "{'name':'URL', 'type':'str', 'value':'%s'}" % \
                            ( publicURL )
        valuesJson += "]}"
        message_obj['values'] = valuesJson
        bq_data_insert( BQ, message_obj, deviceId, PROJECT, DATASET, TABLE )

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.critical( "Exception in save_image(): %s" % e)
        traceback.print_tb( exc_traceback, file=sys.stdout )


#------------------------------------------------------------------------------
# Parse and save the (json/dict) data
def save_data( BQ, pydict, deviceId, PROJECT, DATASET, TABLE ):

    if messageType_Image == validateMessageType( pydict ):
        logging.error('save_data: does not handle images.' )
        return 

    # insert into BQ (Env vars and command replies)
    bq_data_insert( BQ, pydict, deviceId, PROJECT, DATASET, TABLE )


#------------------------------------------------------------------------------
# Insert data into our bigquery dataset and table.
def bq_data_insert( BQ, pydict, deviceId, PROJECT, DATASET, TABLE ):
    try:
        # Generate the data that will be sent to BigQuery for insertion.
        # Each value must be a row that matches the table schema.
        rowList = []
        if not makeBQRowList( pydict, deviceId, rowList ):
            return False
        rows_to_insert = []
        for row in rowList:
            rows_to_insert.append( row )
        logging.info( "bq insert rows: %s" % ( rows_to_insert ))

        dataset_ref = BQ.dataset( DATASET, project=PROJECT )
        table_ref = dataset_ref.table( TABLE )
        table = BQ.get_table( table_ref )               

        response = BQ.insert_rows( table, rows_to_insert )
        logging.info( 'bq response: {}'.format( response ))

#debugrob: I need to look up the the user by deviceId, and find their openag flag (or role), to know the correct DATASET to write to.

        return True

    except Exception as e:
        logging.critical( "bq_data_insert: Exception: %s" % e )
        return False




