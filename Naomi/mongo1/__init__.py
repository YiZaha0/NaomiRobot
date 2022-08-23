from sys import exit as exiter
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from Naomi import MONGO_DB_URI
from Naomi import *
import pymongo

myapp = pymongo.MongoClient(MONGO_DB_URI)
dbx = myapp["AsyncIOMotorCursor"]

federation = dbx['federation']
nm = dbx['Nightmode']

try:
    client = MongoClient(MONGO_DB_URI)
except PyMongoError as f:
    exiter(1)
main_db = client["maindb"]


class MongoDB:

    def __init__(self, collection) -> None:
        self.collection = main_db[collection]

    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    def find_one(self, query):
        result = self.collection.find_one(query)
        if result:
            return result
        return False

    def find_all(self, query=None):
        if query is None:
            query = {}
        return list(self.collection.find(query))

    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    def delete_one(self, query):
        self.collection.delete_many(query)
        return self.collection.count_documents({})

    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def close():
        return client.close()


def __connect_first():
    _ = MongoDB("test")


__connect_first()