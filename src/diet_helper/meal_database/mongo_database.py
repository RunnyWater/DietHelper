import pymongo
from dotenv import load_dotenv
import os


class MongoMealManager:
    def __init__(self, con_string=None, database_name=None, meal_collection_name='meal'):
        if con_string is None or database_name is None:
            load_dotenv()
            # Change to your connection string and database name
            CONNECTION_STRING = os.getenv('CONNECTION_STRING')
            DATABASE_NAME = os.getenv('DATABASE_NAME')
        self.con_string = CONNECTION_STRING
        self.database_name = DATABASE_NAME
        self.meal_collection_name = meal_collection_name
        self.connected = False
        self.client = None

    def connect_to_database(self):
        try:
            client = pymongo.MongoClient(self.con_string)
            self.connected = True
            return client
        except Exception as e:
            print( "There was an error while connecting to database: " + str(e))
            return 404        

    def get_collection(self):
        self.client = self.connect_to_database()
        try:
            db = self.client[f'{self.database_name}']
            return db[f'{self.meal_collection_name}']
        except Exception as e:
            self.close_connection()
            print( "There was an error while getting collection: " + str(e))
            return 404

    def get_meals(self):
        meals_collection = self.get_collection()
        try: 
            meals = meals_collection.find()
            return meals
        except Exception as e:
            self.close_connection()
            print( "There was an error while getting meals: " + str(e))
            return 404

    def add_food(self, id:int, new_food:dict) -> str:
        meal_collection = self.get_collection()
        if meal_collection == 404:
            return 404
        try:
            foods = meal_collection.find_one({"_id": id})["foods"]
            foods.update(new_food)
            meal_collection.update_one({"_id": id}, {"$set":{"foods":foods}})
            self.close_connection()
        except Exception as e:
            self.close_connection()
            print("There was an error while adding new food: " + str(e))
            return 404

    def insert_meal(self, foods:dict) -> str:
        meal_collection = self.get_collection()
        if meal_collection == 404:
            return 404
        try:
            last_document = meal_collection.find().sort("_id", -1).limit(1).next()
            if last_document:
                id = last_document['_id']+1
            else:
                id = 0
            meal_collection.insert_one({"_id": id, "foods":foods})
            self.close_connection()
            return 200
        except Exception as e:
            self.close_connection()
            print("There was an error while adding new meal: " + str(e))
            return 404
        
    def change_food_weight(self, meal_id:int, food_name:str, new_weight:float) -> str:
        meal_collection = self.get_collection()
        try: 
            foods = meal_collection.find_one({"_id": meal_id})['foods']
            if food_name not in foods.keys():
                return f"{food_name} not in meal {meal_id}"
            foods[food_name] = new_weight
            meal_collection.update_one({"_id": meal_id}, {"$set":{"foods":foods}})
            print("Food was successfully updated")
            self.close_connection()
        except Exception as e:
            self.close_connection()
            print( "There was an error while updating food weight inside a meal: " + str(e))
            return 404

    def update_food_name(self, id:int, old_name:str, new_name:str):
        meal_collection = self.get_collection()
        if meal_collection == 404:
            return 404
        try:
            foods = meal_collection.find_one({"_id": id})["foods"]
            foods[new_name] = foods.pop(old_name)
            meal_collection.update_one({"_id": id}, {"$set":{"foods":foods}})
            self.close_connection()
        except Exception as e:
            self.close_connection()
            print("There was an error while adding new food: " + str(e))
            return 404

    def delete_meal(self, id:int) -> str:
        meal_collection = self.get_collection()
        if meal_collection == 404:
            return 404
        try:
            meal_collection.delete_one({"_id": id})
            self.close_connection()
            return 200
        except Exception as e:
            self.close_connection()
            print("There was an error while deleting meal: " + str(e))
            return 404

    def delete_food(self, id:int, food_name:str) -> str:
        meal_collection = self.get_collection()
        if meal_collection == 404:
            return 404
        try:
            foods = meal_collection.find_one({"_id": id})["foods"]
            foods.pop(food_name)
            meal_collection.update_one({"_id": id}, {"$set":{"foods":foods}})
            self.close_connection()
            return 200
        except Exception as e:
            self.close_connection()
            print("There was an error while deleting food: " + str(e))
            return 404

    def close_connection(self) -> None:
        try:
            self.client.close()
            self.connected = False
            print("Connection was successfully closed")
        except Exception as e:
            print("There was an error while closing connection: " + str(e))