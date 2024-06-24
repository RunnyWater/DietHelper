from .meal import Meal
from .meal_database import MongoMealManager, JsonMealManager

class Meals:
    def __init__(self, db_type:str='json', json_file_path:str='json/meals.json'):
        self.db_type = db_type
        if db_type == 'json':
            self.__manager = JsonMealManager(json_file_path=json_file_path)
            self.meals = self.get_meals_json()
            self.json_file_path = json_file_path
        elif db_type == 'mongo':
            self.__manager = MongoMealManager()
            self.meals = self.get_meals_mongo()
                
    
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


    def get_meals_json(self):
        meal_list = self.__manager.get_meals()
        meals = {}
        for meal_id in meal_list.keys():
            meals.update({meal_id:Meal(meal_id, meal_list[meal_id], json_file_path=self.json_file_path)})
        return meals
    

    def get_meal_by_id(self, id:int):
        return self.meals[id]
    

    def insert_meal(self, foods:dict):
        if len(self.meals) == 0:
            id = 0
        else:
            id = max(self.meals.keys()) + 1
        if self.db_type == 'json':
            self.meals.update({id:Meal(id, foods, json_file_path=self.json_file_path)})
        elif self.db_type == 'mongo':
            self.meals.update({id:Meal(id, foods)})
        self.__manager.insert_meal(foods)
        return f"Meal added"
    
    
    def change_food_weight(self, id:int, food_name:str, new_weight:int):
        self.meals[id].change_food_weight(food_name, new_weight)
        self.__manager.change_food_weight(id, food_name, new_weight)
        return f"Food {food_name} weight changed in meal {id}"


    def delete_meal(self, id:int):
        self.meals.pop(id)
        self.__manager.delete_meal(id)
        return f"Meal {id} deleted"
    

    def delete_food(self, id:int, food_name:str):
        self.meals[id].delete_food(food_name)
        self.__manager.delete_food(id, food_name)
        return f"Food {food_name} deleted from meal {id}"
    
    def __repr__(self) -> str:
        return ', '.join([str(meal) for meal in self.meals.values()])