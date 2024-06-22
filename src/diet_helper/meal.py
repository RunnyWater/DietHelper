from .food_database import MongoFoodManager, JsonFoodManager
from .calculator import * 

class Meal:
    def __init__(self, id, foods={}, db_type='json', json_file_path='json/foods.json'):
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
               return self.update_weight(food_name, weight)
            elif input("Do you want to add another food? (y/n)") == 'n':
                return f"{food_name} already in the meal"
        self.foods[food_name] = weight
        food = self.__manager.get_food(food_name)
        self.update_macros(food_name, weight, food['p'], food['f'], food['c'])
        self.__manager.close_connection()
        return f"{food_name} added to meal with weight {weight}"

    
    def update_weight(self, food_name:str, new_weight:int):
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


    def set_weight(self, food_name, new_weight):
        self.foods[food_name] = new_weight
        return f"Weight of {food_name} updated to {new_weight}"


    def update_macros(self, weight, p, f, c, sign=1):
        self.sum_of_proteins += get_proteins(weight, p)*sign
        self.sum_of_fats +=     get_fats(weight, f)*sign
        self.sum_of_carbs +=    get_carbs(weight, c)*sign
        self.sum_of_calories += get_calories(weight, p, f, c)*sign


    def get_foods(self):
        return list(self.foods.keys())


    def __repr__(self) -> str:
        return self.foods


    def __str__(self) -> str:
        return f"{self.foods}"
    
    '''
    Due to it leading to really big memory usage in the long run
    I do not recommend using note function:
     - FREE tier MongoDB
     - Limited memory on your server if you're using other database
     - notes with very long text
     If nevertheless you have a need for it, you can use it with note compression package''' # TODO: add connection to note managing package
    # def add_note(self, note):
    #     note = str(note)
    #     if self.note != '':
    #         input = ''
    #         while(input not in ['a', 'u', 'exit']):
    #             input = input("Do you want 'add to' or 'update' note? (a/u), or type 'exit' if you want to exit").lower()
    #         if input == 'u':
    #             self.note = note
    #         elif input == 'a':
    #             self.note = self.note + '\n' + note
    #     else:
    #         self.note = note
    #     return f"Note added to meal: {self.note}"

    
    # def dekete_note(self):
    #     if self.note != '':
    #         self.note = ''
    #         return f"Note deleted from meal"
    #     else:
    #         return f"No note in meal"
        

    # def get_note(self):
    #     return self.note

