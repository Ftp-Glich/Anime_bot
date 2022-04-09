import pymongo


class Searcher(object):
    def __init__(self):
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017")
        self.current_db = self.db_client["pylougedb"]
        self.collection = self.current_db["animes_db"]

    def get_res(self, genres):
        result = self.search(genres)
        return result

    def search(self, genres):
        res = list()
        temp = 0
        for doc in self.collection.find():
            if temp == 1135:
                break
            gen = doc["genres" + str(temp)]
            k = list(set(gen) & set(genres))
            if sorted(genres) == sorted(k):
                res.append(doc["href" + str(temp)])
            temp += 1
        return res
