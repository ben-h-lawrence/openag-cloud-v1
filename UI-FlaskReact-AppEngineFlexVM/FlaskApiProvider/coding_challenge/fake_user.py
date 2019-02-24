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
        user = FakeUser.fetch({'username': self.username})
        if not user:
            return None, None
        if not pbkdf2_sha256.verify(self.password, user.get('password', '')):
            return None, None
        user_uuid = user.get('user_uuid')
        is_admin = user.get('is_admin', False)
        return user_uuid, is_admin

    @staticmethod
    def fetch(keys):
        return db.query('Users', keys)

    @staticmethod
    def change_password(user_uuid, new_password):
        encrypted_password = pbkdf2_sha256.hash(new_password)
        return db.update('Users', {'password': encrypted_password}, {'user_uuid': user_uuid})


User = FakeUser
