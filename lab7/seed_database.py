from pymongo import MongoClient
from encryption import cypher_suite, encrypt

client = MongoClient()

client = MongoClient('localhost', 27017)

db = client['lab7_db']
users_collection = db['users-collection']

if users_collection.count_documents({}) == 0:
    users = [
        {
            'username': 'greelio',
            'secret_key': '123231'
        },
        {
            'username': 'vasea',
            'secret_key': '4341234'
        },
        {
            'username': 'slavi13',
            'secret_key': '315454'
        },
        {
            'username': 'alisa',
            'secret_key': '512343'
        },
        {
            'username': 'bob',
            'secret_key': '12343'
        }
    ]

    for user in users:
        user['secret_key'] = encrypt(user['secret_key'])

    users_collection.insert_many(users)