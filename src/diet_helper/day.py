from .meals import Meals
from datetime import datetime

class Day:
    def __init__(self,meal_ids:set, date:datetime, db_type = 'json', json_file_path = 'json/meals.json'):
        self.db_type = db_type
        self.json_file_path = json_file_path
        self.meals = Meals(db_type=self.db_type, json_file_path=self.json_file_path)
        self.sum_of_proteins = 0
        self.sum_of_fats = 0
        self.sum_of_carbs = 0
        self.sum_of_calories = 0

        self.meal_ids = set(meal_ids)
        if len(self.meal_ids)> 0:
            for meal_id in self.meal_ids:
                if meal_id not in set(self.meals.meals.keys()):
                    exit('There was an error while gettting meal_ids from database')
                macros = self.meals.get_meal_by_id(meal_id).get_macros()
                p = macros['p']
                f = macros['f']
                c = macros['c']
                cal += macros['cal']
                self.update_macros(p, f, c, cal)
        self.date = date


    def update_macros(self, p:float, f:float, c:float, cal:float, sign:int=1):
        self.sum_of_proteins += p * sign
        self.sum_of_fats += f * sign
        self.sum_of_carbs += c * sign
        self.sum_of_calories += cal * sign

    def add_meal(self, meal_id:int):
        if meal_id not in set(self.meals.meals.keys()):
            return 404
        self.meal_ids.append(meal_id)
        macros = self.meals.get_meal_by_id(meal_id).get_macros()
        p = macros['p']
        f = macros['f']
        c = macros['c']
        cal += macros['cal']
        self.update_macros(p, f, c, cal)
        print("Meal added successfully")
        return 200

    def change_date(self, new_date:datetime):
        self.date = new_date

    def delete_meal(self, id:int):
        self.meal_ids.remove(id)
        macros = self.meals.get_meal_by_id(id).get_macros()
        p = macros['p']
        f = macros['f']
        c = macros['c']
        cal -= macros['cal']
        self.update_macros(p, f, c, cal, sign=-1)
