from sqlalchemy import Table, Column, Integer, MetaData, String, TIMESTAMP, Float

from utils import send_email

metadata_obj = MetaData()

class User:
    def __init__(self, login, email, password) -> None:
        self.login = login
        self.email = email
        self.password = password
        self.is_confirmed = False
        self.confirmation_code =  None