from FCClass.account_recovery_request import AccountRecoveryRequest
from . import lil_db as db
from google.cloud import datastore
from datetime import datetime,timedelta
import uuid

class FakeAccountRecoveryRequest:
    def __init__(self, user_uuid):
        self.user_uuid = user_uuid
        self.recovery_token = str(uuid.uuid4())
        self.created_date = datetime.now()
        self.expiration_date = self.created_date + timedelta(hours=24)

    def insert_into_db(self,client):
        recovery_request = {
            'user_uuid': self.user_uuid,
            'recovery_token': self.recovery_token,
            'expiration_date': self.expiration_date
        }
        db.write('AccountRecoveryRequest', recovery_request)
        return self.recovery_token

    @staticmethod
    def fetch(client, recovery_token):
        recovery_request = {
            'recovery_token': recovery_token
        }
        result = db.query('AccountRecoveryRequest', recovery_request)
        return result

    @staticmethod
    def delete(client, recovery_token):
        recovery_request = {
            'recovery_token': recovery_token
        }
        result = db.delete('AccountRecoveryRequest', recovery_request)
        return result


AccountRecoveryRequest = FakeAccountRecoveryRequest
