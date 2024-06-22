from meal import Meal
from meal_database import MongoMealManager

class Meals:
    def __init__(self, db_type='json', json_file_path='json/meals.json'):
        if db_type == 'json':
            self.meals = [] # TODO: load from json
        elif db_type == 'mongo':
            self.__manager = MongoMealManager()
            self.foods = self.get_meals_mongo()
                
    
    def get_meals_mongo(self):
        meals_list = self.__manager.get_meals()
        try: 
            meals = {}
            for meal in meals_list:
                meals.update({meal['_id']:Meal(meal['_id'], meal['foods'], db_type='mongo')})
            return meals
        
        except Exception as e:
            print( "There was an error while getting meals from MongoDB: " + str(e))
            return None