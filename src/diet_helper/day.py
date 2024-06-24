from meals import Meals
from datetime import datetime

class Day:
    def __init__(self,meals, date=None, db_type = 'json', json_file_path = 'json/meals.json'):
        self.db_type = db_type
        self.json_file_path = json_file_path
        self.meals = Meals(db_type=self.db_type, json_file_path=self.json_file_path)
        if len(meals)> 0:
            for meal_id in set(meals):
                if meal_id not in set(self.meals.meals.keys()):
                    exit('There was an error while gettting meal_ids from database')
        self.meal_ids = meals
        if date != None and self.is_date_in_format(date):
            self.date = date
        elif date == None:
            self.date = self.get_todays_date()
        self.sum_of_proteins = 0
        self.sum_of_fats = 0
        self.sum_of_carbs = 0
        self.sum_of_calories = 0


    def update_macros(self, weight, p, f, c, sign=1):
        for meal_id in self.meal_ids:
            macros = self.meals.get_meal_by_id(meal_id).get_macros(weight, p, f, c, sign=sign)
            self.sum_of_proteins += macros['p']
            self.sum_of_fats += macros['f']
            self.sum_of_carbs += macros['c']
            self.sum_of_calories += macros['cal']

    def add_meal(self, meal_id:int):
        if meal_id not in set(self.meals.meals.keys()):
            return 404
        self.meal_ids.append(meal_id)

    def get_todays_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def change_date(self, new_date:str):
        if new_date == None:
            print('New date has not been provided')
        self.date = new_date

    def is_date_in_format(self, date:str):
        try :
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False