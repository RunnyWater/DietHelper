import pymongo 
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

class MongoDayManager:
    def __init__(self, con_string=None, database_name=None, day_collection_name='day'):
        if con_string is None or database_name is None:
            load_dotenv()
            
            self.con_string = os.getenv('CONNECTION_STRING')
            self.database_name = os.getenv('DATABASE_NAME')
        else:
            self.con_string = con_string
            self.database_name = database_name
        self.day_collection_name = day_collection_name
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
            return db[f'{self.day_collection_name}']
        except Exception as e:
            self.close_connection()
            return "There was an error while getting collection: " + str(e)

    def close_connection(self, print_stages: bool = False) -> None:
        try:
            self.client.close()
            self.connected = False
            if print_stages: print("Connection was successfully closed")
        except Exception as e:
            print("There was an error while closing connection: " + str(e))

    def get_days(self):
        day_collection = self.get_collection()
        try: 
            days = day_collection.find()
            return days
        except Exception as e:
            self.close_connection()
            return "There was an error while getting days: " + str(e)

    def get_day(self, day:datetime):
        date = self.get_start_of_the_day(day)
        day_collection = self.get_collection()
        try: 
            day = day_collection.find_one({"_id":date})
            return day
        except Exception as e:
            self.close_connection()
            return "There was an error while getting food: " + str(e)

    def get_days_by_month(self, month:int = datetime.now().month, year:int = datetime.now().year):
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        days = self.get_days_between_two_dates(start_date, end_date)
        return days
    
    def get_days_between_two_dates(self, start_date:datetime, end_date:datetime):  
        day_collection = self.get_collection()
        try: 
            days = day_collection.find({
                "_id": {
                    "$gte": start_date,
                    "$lt": end_date
                }
            })
            return days
        except Exception as e:
            self.close_connection()
            print( "There was an error while getting days: " + str(e))
            return None

    def get_todays_date(self):
        return datetime.combine(datetime.today(), datetime.min.time())

    def add_day(self, day:datetime = None, meals:list[dict] = [], print_stages: bool = False):
        if day is None:
            date = self.get_start_of_the_day(self.get_todays_date())
        else:
            date = self.get_start_of_the_day(day)
        day_collection = self.get_collection()
        if day_collection.count_documents({"_id": date}) > 0:
            print("Day already exists")
            return None
        try: 
            day_collection.insert_one({'_id':date, 'meals':meals})
            if print_stages: print("Day added successfully")
            return None
        except Exception as e:
            self.close_connection()
            print("There was an error while adding day: " + str(e))
            return 404

    def add_meal(self, day:datetime = None, meal:dict = {}, print_stages: bool = False):
        if day is None:
            date = self.get_start_of_the_day(self.get_todays_date())
        else:
            date = self.get_start_of_the_day(day)
        day_collection = self.get_collection()
        try:
            day_collection.update_one({"_id": date}, {"$push": {"meals": meal}}) # pushing meal to day's meals list
            if print_stages: print("Meal added successfully to day")
            return None
        except Exception as e:
            self.close_connection()
            print( "There was an error while adding meal: " + str(e))
            return 404
        
    def get_meals_by_day(self, day:datetime  = None):
        if day is None:
            date = self.get_start_of_the_day(self.get_todays_date())
        else:
            date = self.get_start_of_the_day(day)
        day_collection = self.get_collection()
        try: 
            day = day_collection.find_one({"_id": date})
            return day['meals']
        except Exception as e:
            self.close_connection()
            print( "There was an error while getting meals: " + str(e))
            return None
        
    def get_start_of_the_day(self, day:datetime):
        return datetime.combine(day, datetime.min.time())
    
    def add_food_to_day(self, day:datetime, meal_number:int, food:str, weight:float, print_stages: bool = False):
        meal_number = meal_number - 1
        date = self.get_start_of_the_day(day)
        day_collection = self.get_collection()
        try:
            day_doc = day_collection.find_one({"_id": date})

            # If the day document does not exist, return a 404 error
            if not day_doc:
                print("Day does not exist")
                return 404
            else:
                meals = day_doc["meals"]
                # Ensure the meals array has enough length
                if len(meals) < meal_number + 1:
                    print("Meal does not exist")
                    return 404
                else:
                    # Add the new food to the meal
                    meal = meals[meal_number]
                    meal[food] = weight
                    day_collection.update_one({"_id": date}, {"$set": {"meals": meals}})
            if print_stages: print("Food added successfully to meal")
            return None
        except Exception as e:
            self.close_connection()
            print( "There was an error while adding food: " + str(e))
            return 404
    

    def change_food_weigth_in_meal(self, day:datetime, meal_number:int, food:str, weight:float, print_stages: bool = False):
        meal_number = meal_number - 1
        date = self.get_start_of_the_day(day)
        day_collection = self.get_collection()
        try:
            day_doc = day_collection.find_one({"_id": date})

            # If the day document does not exist, return a 404 error
            if not day_doc:
                print("Day does not exist")
                return 404
            else:
                meals = day_doc["meals"]
                # Ensure the meals array has enough length
                if len(meals) < meal_number + 1:
                    print("Meal does not exist")
                    return 404
                else:
                    # Change the weight of the food
                    meal = meals[meal_number]
                    if food not in meal:
                        print("Food does not exist")
                        return 404
                    else:
                        meal[food] = weight
                        day_collection.update_one({"_id": date}, {"$set": {"meals": meals}})
            if print_stages: print("Food weight changed successfully")
            return None
        except Exception as e:
            self.close_connection()
            print( "There was an error while adding food: " + str(e))
            return 404


    def delete_food_from_meal(self, day:datetime, meal_number:int, food:str, print_stages: bool = False):
        meal_number = meal_number - 1
        date = self.get_start_of_the_day(day)
        day_collection = self.get_collection()
        try:
            day_doc = day_collection.find_one({"_id": date})

            # If the day document does not exist, return a 404 error
            if not day_doc:
                print("Day does not exist")
                return 404
            else:
                meals = day_doc["meals"]
                # Ensure the meals array has enough length
                if len(meals) < meal_number + 1:
                    print("Meal does not exist")
                    return 404
                else:
                    # Delete the new food from the meal
                    meal = meals[meal_number]
                    meal.pop(food)
                    day_collection.update_one({"_id": date}, {"$set": {"meals": meals}})
            if print_stages: print("Food added successfully to meal")
            return None
        except Exception as e:
            self.close_connection()
            print( "There was an error while adding food: " + str(e))
            return 404
