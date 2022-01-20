# -*- coding: utf-8 -*-


import pymongo


class UserBase:
    def __init__(self):
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017")
        self.current_db = self.db_client["pylougedb"]
        self.collection = self.current_db["users_db"]

    def add_user(self, user_id, platform):
        temp = {
                "user_id": user_id,
                "platform": platform,
                "search_list": [],
                "message_id": int(),
                "chat_id": int(),
                "results": []
                }
        self.collection.insert(temp)

    def get_platform(self, user_id):
        res = self.collection.find_one({"user_id": user_id})
        if res is None:
            return 0
        return res["platform"]

    def get_search_list(self, user_id):
        res = self.collection.find_one({"user_id": user_id})
        return res["search_list"]

    def append_to_search_list(self, user_id, element):
        res = self.collection.find_one({"user_id": user_id})
        res["search_list"].append(element)
        self.collection.delete_one({"user_id": user_id})
        self.collection.insert(res)

    def clear_search_list(self, user_id):
        res = self.collection.find_one({"user_id": user_id})
        res["search_list"] = []
        self.collection.delete_one({"user_id": user_id})
        self.collection.insert(res)

    def get_message_id(self, user_id):
        res = self.collection.find_one({"user_id": user_id})
        return res["message_id"]

    def set_message_id(self, user_id, message_id):
        res = self.collection.find_one({"user_id": user_id})
        res["message_id"] = message_id
        self.collection.delete_one({"user_id": user_id})
        self.collection.insert(res)

    def set_results(self, user_id, results):
        res = self.collection.find_one({"user_id": user_id})
        res["results"] = results
        self.collection.delete_one({"user_id": user_id})
        self.collection.insert(res)

    def clear_results(self, user_id):
        res = self.collection.find_one({"user_id": user_id})
        res["results"].clear()
        self.collection.delete_one({"user_id": user_id})
        self.collection.insert(res)

    def get_results(self, user_id):
        res = self.collection.find_one({"user_id": user_id})
        return res["results"]

    def set_chat_id(self, user_id, chat_id):
        res = self.collection.find_one({"user_id": user_id})
        res["chat_id"] = chat_id
        self.collection.delete_one({"user_id": user_id})
        self.collection.insert(res)

    def get_chat_id(self, user_id):
        res = self.collection.find_one({"user_id": user_id})
        return res["chat_id"]
