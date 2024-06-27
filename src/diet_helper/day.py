from datetime import datetime

class Day:
    def __init__(self,meal_ids:list, date:datetime, db_type = 'json', json_file_path = 'json/meals.json'):
        self.db_type = db_type
        self.json_file_path = json_file_path
        self.sum_of_proteins = 0
        self.sum_of_fats = 0
        self.sum_of_carbs = 0
        self.sum_of_calories = 0
        self.meal_ids = meal_ids
        self.date = self.get_normalized_date(date)


    def update_macros(self, p:float, f:float, c:float, cal:float, sign:int=1):
        self.sum_of_proteins += p * sign
        self.sum_of_fats += f * sign
        self.sum_of_carbs += c * sign
        self.sum_of_calories += cal * sign

    def add_meal(self, meal_id:int, macros:dict)-> int:
        self.meal_ids.append(meal_id)
        p = macros['p']
        f = macros['f']
        c = macros['c']
        cal = macros['cal']
        self.update_macros(p, f, c, cal)
        print("Meal added successfully")
        return 200

    def set_date(self, new_date:datetime):
        date = self.get_normalized_date(new_date)
        self.date = date
        print("Date set successfully")

    def delete_meal(self, id:int, macros:dict):
        if id not in self.meal_ids:
            print("Meal does not exist in this day")
            return
        self.meal_ids.remove(id)
        p = macros['p']
        f = macros['f']
        c = macros['c']
        cal = macros['cal']
        self.update_macros(p, f, c, cal, sign=-1)


    def get_normalized_date(self, date:datetime):
        return datetime.combine(date, datetime.min.time())