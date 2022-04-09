import pymongo


class Updater:
    def __init__(self):
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017")
        self.current_db = self.db_client["pylougedb"]
        self.collection = self.current_db["animes_db"]

    def update(self, mass):
       self.collection.delete_many({})
       self.collection.insert_many(mass)
