import pymongo
from dict import Dictionary

animes = Dictionary()

animes_array = animes.get_animes()

db_client = pymongo.MongoClient("mongodb://localhost:27017")

current_db = db_client["pylougedb"]

collection = current_db["animes_db"]

ins_result = collection.insert_many(animes_array)

