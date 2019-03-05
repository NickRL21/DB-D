import psycopg2
from dbd_api.database_helper import Database
from passlib.apps import custom_app_context as pwd_context

def user_exists(dci_number):
    pass

def hash(self, password):
    self.password_hash = pwd_context.encrypt(password)


def verify(self, password):
     return pwd_context.verify(password, self.password_hash)
