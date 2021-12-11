from pymongo import MongoClient

client = MongoClient()

client = MongoClient('localhost', 27017)

#client.drop_database('lab7_db')

db = client['lab7_db']
users_collection = db['users-collection']