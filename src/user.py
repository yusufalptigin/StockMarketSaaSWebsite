from flask import current_app
from flask_login import UserMixin
import jwt
import time

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    @property
    def is_active(self):
        return self.active
    
    def get_id(self):
        return self.username

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.username, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return None
        print(data, "data")
        print(get(data['id']))
        return get(data['id'])


def get(user_id):
    db = current_app.config["db"]
    return db.get_user(user_id)


def verify(username, password):
    db = current_app.config["db"]
    return db.verify_user(username, password)
