import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    'mongodb+srv://test1:123@cluster0.hfj9h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['Flame']
collection = db['arjdoroteo']

results = collection.find().sort('_id', -1).limit(1)

for result in results:
    print(result)
