from FCClass.user_session import UserSession
from . import lil_db as db

class FakeUserSession(UserSession):
    def insert_into_db(self,client):
        session = {
            'user_uuid': self.user_uuid,
            'session_token': self.session_token,
            'created_date': self.created_date,
            'expiration_date': self.expiration_date
        }
        db.write('UserSession', session)
        return self.session_token

UserSession = FakeUserSession
