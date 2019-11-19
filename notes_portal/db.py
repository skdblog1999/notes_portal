import pymongo

db_connection = pymongo.MongoClient(
    "mongodb://localhost:27017/?readPreference=primary")
database = db_connection["notes_portal"]
