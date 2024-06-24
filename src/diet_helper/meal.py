from .food_database import MongoFoodManager, JsonFoodManager
from .calculator import * 

class Meal:
    def __init__(self, id:int, foods:dict={}, db_type:str='json', json_file_path:str='json/foods.json'):
        self.id = id
        self.foods = foods
        self.sum_of_proteins = 0
        self.sum_of_fats = 0
        self.sum_of_carbs = 0
        self.sum_of_calories = 0
        if len(foods) > 0:
            if db_type == 'json':
                self.__manager = JsonFoodManager(json_file_path=json_file_path)
                foods = self.__manager.get_foods()
                for food in self.foods:
                    self.update_macros(self.foods[food], foods[food]['p'], foods[food]['f'], foods[food]['c'])
            elif db_type == 'mongo': 
                self.__manager = MongoFoodManager()
                food_collection = self.__manager.get_collection()
                for food_name in self.foods.keys():
                    food = food_collection.find_one({"name":food_name.lower()})
                    self.update_macros(self.foods[food_name], food['p'], food['f'], food['c'])
                self.__manager.close_connection()
        else:
            if db_type == 'json':
                self.__manager = JsonFoodManager()
            elif db_type == 'mongo': 
                self.__manager = MongoFoodManager()
    

    def add_food(self, food_name:str, weight:int):
        food_name
        if food_name in list(self.foods.keys()):
            if input( "This food is already in meal, do you want to update its weight? (y/n)") == 'y':
               return self.change_food_weight(food_name, weight)
            elif input("Do you want to add another food? (y/n)") == 'n':
                return f"{food_name} already in the meal"
        self.foods[food_name] = weight
        food = self.__manager.get_food(food_name)
        self.update_macros(food_name, weight, food['p'], food['f'], food['c'])
        self.__manager.close_connection()
        return f"{food_name} added to meal with weight {weight}"

    
    def change_food_weight(self, food_name:str, new_weight:int):
        old_weight = self.get_weight(food_name)
        difference = round(new_weight - old_weight, 2)
        food = self.__manager.get_food(food_name)
        self.update_macros(food_name, difference, food['p'], food['f'], food['c'])
        self.set_weight(food_name, new_weight)
        self.__manager.close_connection()
        return f"Weight of {food_name} updated from {old_weight} to {new_weight}"


    def delete_food(self, food_name:str):
        old_weight = self.get_weight(food_name)
        del self.foods[food_name]
        self.update_macros(food_name, old_weight, -1)
        return f"{food_name} deleted from meal"


    def get_weight(self, food_name:str):
        return self.foods[food_name]

    def get_info_for_json(self):
        return {
            'id':self.id,
            'foods':self.foods
        }

    def set_weight(self, food_name, new_weight):
        self.foods[food_name] = new_weight
        return f"Weight of {food_name} updated to {new_weight}"


    def update_macros(self, weight, p, f, c, sign=1):
        self.sum_of_proteins += get_proteins(weight, p)*sign
        self.sum_of_fats +=     get_fats(weight, f)*sign
        self.sum_of_carbs +=    get_carbs(weight, c)*sign
        self.sum_of_calories += get_calories(weight, p, f, c)*sign


    def get_foods(self) -> list:
        return list(self.foods.keys())
    
    def get_macros(self) -> dict:
        return {
            "p": self.sum_of_proteins,
            "f": self.sum_of_fats,
            "c": self.sum_of_carbs,
            "cal": self.sum_of_calories
        }

    def __repr__(self) -> str:
        return self.foods


    def __str__(self) -> str:
        return f"{self.foods}"
    