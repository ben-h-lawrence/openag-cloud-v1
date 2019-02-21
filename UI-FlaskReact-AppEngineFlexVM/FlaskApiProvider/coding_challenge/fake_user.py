import json
import datetime

from FCClass.user import User
from . import lil_db as db
from passlib.hash import pbkdf2_sha256

class FakeUser(User):
    def insert_into_db(self,client):
        new_user = {
            'username': self.username,
            'email_address': self.email_address,
            'password': self.encrypted_password,
            'date_added': datetime.datetime.now(),
            'organization': self.organization,
            'user_uuid':self.user_uuid,
            'is_verified': True
        }
        db.write('Users', new_user)
        return self.user_uuid

    def login_user(self,client):
        result = db.query('Users', username=self.username)
        if not result:
            return None, None
        if not pbkdf2_sha256.verify(self.password, result.get('password', '')):
            return None, None
        user_uuid = result.get('user_uuid')
        is_admin = result.get('is_admin', False)
        return user_uuid, is_admin

User = FakeUser
