from pymongo import *
from collections import OrderedDict


class Mongo:
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super().__new__(self)
        return self.instance

    def __init__(self):
        self.client = MongoClient()

    def getDatabases(self):
        databases = self.client.list_database_names()
        databases.remove('admin')
        databases.remove('config')
        databases.remove('local')
        return databases

    def getCollections(self):
        collections = self.client[self.database.name].list_collection_names()
        return collections

    def getDocuments(self):
        documents = []
        collection = self.collection.find()
        for document in collection:
            documents.append(document)
        return documents

    def getDocumentsID(self):
        documentsID = []
        documents = self.getDocuments()
        for document in documents:
            documentsID.append(document["_id"])
        return documentsID

    def getFields(self):
        documents = self.getDocuments()
        fields = documents[self.document].keys()
        fields = list(fields)
        fields.remove("_id")
        return fields

    def getFieldDataType(self):
        fieldTypes = self.collection.aggregate([{
            "$project": {
                "_id": 0,
                "fieldType": {"$type": "$" + self.field}
            }
        }])
        fieldType = list(fieldTypes)[self.document]
        fieldType = fieldType["fieldType"]
        return fieldType

    def setDatabase(self, database):
        self.database = self.client[database]

    def setCollection(self, collection):
        self.collection = self.database[collection]

    def setDocument(self, document):
        self.document = document

    def setField(self, field):
        self.field = field

    def getStringLengths(self):
        lengths = self.collection.aggregate([{
            "$project": {
                "_id": 0,
                "length": {"$strLenBytes": "$" + self.field}
            }
        }])
        return lengths

    def findStringMinLength(self):
        lengths = self.getStringLengths()
        minLength = len(self.collection.find_one()[self.field])
        for length in lengths:
            lng = length["length"]
            if lng < minLength:
                minLength = lng
        return minLength

    def findStringMaxLength(self):
        lengths = self.getStringLengths()
        maxLength = 0
        for length in lengths:
            lng = length["length"]
            if lng > maxLength:
                maxLength = lng
        return maxLength

    def setStringLength(self, minLength, maxLength):
        schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "properties": {
                    self.field: {
                        "bsonType": "string",
                        "minLength": minLength,
                        "maxLength": maxLength,
                        "description": "Must be between {} and {} character length".format(minLength, maxLength)
                    }
                }
            }
        }
        query = [('collMod', self.collection.name), ('validator', schema), ('validationLevel', 'moderate')]
        query = OrderedDict(query)
        self.database.command(query)

    def findMinValue(self):
        minValue = self.collection.find_one({self.field: {"$exists": True}}, sort=[(self.field, ASCENDING)])
        minValue = minValue[self.field]
        return minValue

    def findMaxValue(self):
        maxValue = self.collection.find_one({self.field: {"$exists": True}}, sort=[(self.field, DESCENDING)])
        maxValue = maxValue[self.field]
        return maxValue

    def setNumberInterval(self, minValue, maxValue):
        schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "properties": {
                    self.field: {
                        "bsonType": "number",
                        "minimum": minValue,
                        "maximum": maxValue,
                        "description": "Must be a value between {} and {}".format(minValue, maxValue)
                    }
                }
            }
        }
        query = [('collMod', self.collection.name), ('validator', schema), ('validationLevel', 'moderate')]
        query = OrderedDict(query)
        self.database.command(query)
