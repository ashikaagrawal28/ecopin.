import pymongo
import certifi
import os

ca = certifi.where()
mongoclient = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=ca)
print("Connected to MongoDB")

database = mongoclient["ecopin"]
collections = {"users": database["users"], "reports": database["reports"]}

class MongoFunc:
    def insert_data(collection, filter):
        collections[collection].insert_one(filter)

    def get_data(collection, filter):
        return collections[collection].find_one(filter)
    
    def find_data(collection, filter):
        return collections[collection].find(filter)
    
    def delete_data(collection, filter):
        collections[collection].delete_one(filter)

    def update_data(collection, filter, new_values):
        collections[collection].update_one(filter, {"$set": new_values})

    def add_points(email, points):
        user = MongoFunc.get_data('users', {'email': email})
        if user is not None:
            new_points = user['points'] + points
            MongoFunc.update_data('users', {'email': email}, {'points': new_points})
            return new_points
        return None