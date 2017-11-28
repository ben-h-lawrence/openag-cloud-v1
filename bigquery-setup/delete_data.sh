#!/bin/bash

source gcloud_env.bash

list_ds_and_tables

#------------------------------------------------------------------------------
# Command line arg processing
if [ $# -lt 2 ]; then
  echo "Please provide the dataset and table to remove data from."
  echo "For example: openag_private_webui user"
  exit 1
fi
DS=$1
TABLE=$2

#------------------------------------------------------------------------------
# Remove data from the OpenAg PRIVATE internal DATA_DS tables.
rm_data $DS $TBL


