import pymongo

class MongoMealManager:
    def __init__(self, con_string, database_name, food_collection_name='meals'):
        self.con_string = con_string
        self.database_name = database_name
        self.meal_collection_name = food_collection_name
        self.connected = False
        self.client = None

    def connect_to_database(self):
        try:
            client = pymongo.MongoClient(self.con_string)
            self.connected = True
            return client
        except Exception as e:
            return "There was an error while connecting to database: " + str(e)

    def get_collection(self):
        self.client = self.connect_to_database()
        try:
            db = self.client[f'{self.database_name}']
            return db[f'{self.food_collection_name}']
        except Exception as e:
            self.close_connection()
            return "There was an error while getting collection: " + str(e)
    

    def get_meals(self):
        meals_collection = self.get_collection()
        try: 
            meals = meals_collection.find()
            self.close_connection()
            return meals
        except Exception as e:
            self.close_connection()
            return "There was an error while getting meals: " + str(e)


    def insert_meal(self, name=str, p=str != None, f=str != None, c=str != None, variants=None) -> str:
        meal_collection = self.get_collection()
        try: 
            meal_collection.insert_one({"_id": meal_collection.count_documents(), "name":name.lower(), "p":p, "f":f, "c":c, "variants":variants})
            self.close_connection()
            return f"{name} added to database with p: {p}, f: {f}, c: {c}"
        except Exception as e:
            self.close_connection()
            return "There was an error while adding new meal: " + str(e)
        

    def close_connection(self) -> None:
        try:
            self.client.close()
            self.connected = False
            print("Connection was successfully closed")
        except Exception as e:
            print("There was an error while closing connection: " + str(e))
