from dotenv import load_dotenv
from os.path import join, dirname
from cryptography.fernet import Fernet
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
cypher_suite = Fernet(os.environ['key'])


def encrypt(mess):
    return cypher_suite.encrypt(str(mess).encode('ascii'))

def decrypt(mess):
    return cypher_suite.decrypt(mess)