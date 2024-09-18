from .day_database import MongoDayManager, JsonDayManager
from .foods import Foods
from .getting_date import *
from datetime import datetime


def get_normalized_date(date:datetime | str):
    if isinstance(date, str):
        date = datetime.strptime(date[:10], '%Y-%m-%d')
    return str(datetime.combine(date, datetime.min.time()))

def from_string_to_date(date:str | datetime):
    if isinstance(date, str):
        return str(datetime.strptime(date[:10], '%Y-%m-%d'))
    else:
        return get_normalized_date(date)

def get_todays_date():
    return str(datetime.combine(datetime.today(), datetime.min.time()))


class Days:
    def __init__(self, con_string=None, database_name=None, day_collection_name='day', db_type='json'):
        self.foods = Foods(db_type=db_type)
        if db_type == 'mongo':
            self.__manager = MongoDayManager(con_string, database_name, day_collection_name)
            self.days = self.get_days_mongo()
        else:
            self.__manager = JsonDayManager()
            self.days = self.get_days_json()
        if self.days is None:
            exit('There was an error while gettting days from database')

    def get_days_mongo(self):
        days = {}
        for day in self.__manager.get_days(): # getting days from mongo
            meals = day['meals'] # getting meals = list of list of dicts (food : weight)
            days[day['_id']] = Day(meals=meals, date=day['_id'], foods=self.foods) # adding day to days dict

        return days 

    def get_days_json(self):
        json_data = self.__manager.get_days()
        days = {}
        for day in json_data: # getting days from json
            days[day] = Day(meals=json_data[day]['meals'], date=day, foods=self.foods) # adding day to days dict
        return days 


    def add_meal(self):
    
        date = get_choice_date(self.days)

        meals = {}

        print("Now please fill in the meal information: ")
        while True:
            food_name = input("Food name (q for quit): ")
            if food_name == 'q':
                break
            weight = input("Weight (r to restart the food): ")
            if weight== 'r':
                break
            food_weight = int(weight)
            meals[food_name] = food_weight

        self.days[date].add_meal(meals)
        self.__manager.add_meal(date, self.days[date].meals)

    def add_day(self):
        year, month, day = get_user_input_date()
        if year == False or month == False or day == False:
            return
        date = str(datetime(year, month, day))
        meals = {}

        print("Now please fill in the meal information: ")
        while True:
            food_name = input("Food name (q for quit): ")
            if food_name == 'q':
                break
            weight = input("Weight (r to restart the food): ")
            if weight== 'r':
                break
            food_weight = int(weight)
            meals[food_name] = food_weight

        self.__manager.add_day(date, meals)
        self.days[date] = Day(meals, date, self.foods)


    def get_total_macros_by_date(self):
        date = get_choice_date(self.days)
        macros = self.days[date].get_total_macros()
        print(macros)
        return macros
    
    def get_meal_macros_by_date(self):
        date = get_choice_date(self.days)
        meals = self.days[date].meals
        if len(meals) == 0:
            print("There are no meals in this day yet")
            return
        str_meals = '\n'.join([f'{i+1}: {meal}' for i, meal in enumerate(meals)])
        print(str_meals)
        while True:
            user_input = input("Please choose one of the meals (q for exiting): ")
            if user_input == 'q':
                print('Exiting...')
                return
            elif user_input.isdigit() and int(user_input) in range(1, len(meals)+1):
                meal_number = int(user_input)
                break
            else:
                print("Invalid input")
        macros = self.days[date].get_meals_macros(meal_number-1)
        print(macros)
        return macros

    def get_all_meals_macros_by_date(self, date:str | datetime):
        date = from_string_to_date(date)
        if date not in list(self.days.keys()):
            print("Day does not exist")
            return 
        
        macros = self.days[date].get_all_meals_macros()
        print(macros)
        return macros

    def add_food_to_day(self, date:str | datetime, meal_number:int, food_name:str, weight:float):
        date = from_string_to_date(date)
        if date not in list(self.days.keys()):
            print("Day does not exist")
            return
        self.__manager.add_food_to_day(date, meal_number, food_name, weight)
        self.days[date].add_food_to_meal(meal_number, food_name, weight)

    def delete_food_from_day(self, date:str | datetime, meal_number:int, food_name:str):
        date = from_string_to_date(date)
        if date not in list(self.days.keys()):
            print("Day does not exist")
            return
        self.__manager.delete_food_from_meal(date, meal_number, food_name)
        self.days[date].delete_food(meal_number, food_name)


    def change_food_weight(self, date:str | datetime, meal_number:int, food_name:str, new_weight:float):
        date = from_string_to_date(date)
        if date not in list(self.days.keys()):
            print("Day does not exist")
            return
        self.__manager.change_food_weigth_in_meal(date, meal_number, food_name, new_weight)
        self.days[date].change_food_weight(meal_number, food_name, new_weight)
    

    def get_all_meals_by_date(self,date:str | datetime):
        date = from_string_to_date(date)
        if date not in list(self.days.keys()):
            print("Day does not exist")
            return 
        return self.days[date].meals


class RoundedDict(dict):
    def __setitem__(self, key, value):
        if isinstance(value, (int, float)):
            super().__setitem__(key, round(value, 2))
        else:
            super().__setitem__(key, value)

class Day:
    def __init__(self,meals:list[dict], date:datetime, foods: Foods):
        self.foods = foods
        self.meals = meals
        self.date = get_normalized_date(date)
        self.sum_of_fats = RoundedDict({'total': 0})
        self.sum_of_carbs = RoundedDict({'total': 0})
        self.sum_of_proteins = RoundedDict({'total': 0})
        self.sum_of_calories = RoundedDict({'total': 0})
        self.calculate_macros()

    def calculate_macros(self):
        for i, meal in enumerate(self.meals):
            for food_name, weight in meal.items():
                if food_name not in self.foods.get_names():
                    print(f"Food {food_name} does not exist")
                    continue
                self.update_macros(food_name, weight, meal_number=i)
            if len(meal) > 0:
                self.update_days_macros_with_meal(meal_number=i)
            elif len(meal) == 0:
                self.initialize_macros_for_meal(meal_number=i)
        

    def initialize_macros_for_meal(self, meal_number:int):
        self.sum_of_fats[meal_number]       = 0
        self.sum_of_carbs[meal_number]      = 0
        self.sum_of_proteins[meal_number]   = 0
        self.sum_of_calories[meal_number]   = 0

    def update_macros(self, food_name: str, weight: float, meal_number:int,  sign: int = 1):
        # Check if it's the first time meal is added
        if meal_number not in self.sum_of_calories.keys():
            self.initialize_macros_for_meal(meal_number)

        macros = self.foods.get_macros_by_name(food_name)
        self.sum_of_fats[meal_number]       += macros['f']      * weight * sign
        self.sum_of_carbs[meal_number]      += macros['c']      * weight * sign
        self.sum_of_proteins[meal_number]   += macros['p']      * weight * sign
        self.sum_of_calories[meal_number]   += macros['cal']    * weight * sign

    def update_days_macros_with_meal(self, meal_number:int, sign: int = 1):
        self.sum_of_fats['total']       +=    self.sum_of_fats[meal_number]       *     sign
        self.sum_of_carbs['total']      +=    self.sum_of_carbs[meal_number]      *     sign
        self.sum_of_proteins['total']   +=    self.sum_of_proteins[meal_number]   *     sign
        self.sum_of_calories['total']   +=    self.sum_of_calories[meal_number]   *     sign

    def update_days_macros_with_food(self, food_name:str, weight:float, sign: int = 1):
        macros = self.foods.get_macros_by_name(food_name)
        self.sum_of_fats['total']       +=    macros['f']    * weight * sign
        self.sum_of_carbs['total']      +=    macros['c']    * weight * sign
        self.sum_of_proteins['total']   +=    macros['p']    * weight * sign
        self.sum_of_calories['total']   +=    macros['cal']  * weight * sign

    def get_total_macros(self):
        return {
            "p":    self.sum_of_proteins['total'],  
            "f":    self.sum_of_fats['total']    ,  
            "c":    self.sum_of_carbs['total']   ,  
            "cal":  self.sum_of_calories['total'],  
        }
    
    def get_meals_macros(self, meal_number:int):
        return {
            "p":    self.sum_of_proteins[meal_number],  
            "f":    self.sum_of_fats[meal_number]    ,  
            "c":    self.sum_of_carbs[meal_number]   ,  
            "cal":  self.sum_of_calories[meal_number],  
        }

    def get_all_meals_macros(self):
        macros = {}
        for i in range(0, len(self.meals)):
            macros.update({i+1:self.get_meals_macros(i)})
        return macros


    def add_meal(self, meal:dict)-> int:
        self.meals.append(meal)
        for food_name, weight in meal.items():
            if food_name not in self.foods.get_names():
                    print(f"Food {food_name} does not exist")
                    continue
            self.update_macros(food_name, weight, meal_number=len(self.meals))
        self.update_days_macros_with_meal(meal_number=len(self.meals))
        print("Meal added successfully")
        return 200

    def set_date(self, new_date:datetime):
        date = get_normalized_date(new_date)
        self.date = date
        print("Date set successfully")

    def delete_food(self, meal_number:int, food:str):
        meal = self.meals[meal_number]            
        if food in meal:
            old_weight = meal[food]
            self.update_macros(food, old_weight,sign=-1)
            self.update_days_macros_with_food(food,old_weight,sign=-1)
            print("Food deleted successfully")
        else:
            print("Food does not exist")

    def change_food_weight(self, meal_number:int, food:str, new_weight:float):
        meal = self.meals[meal_number]
        if food in meal:
            old_weight = meal[food]
            if old_weight < new_weight:
                self.update_macros(food, new_weight-old_weight,sign=1)
                self.update_days_macros_with_food(food, new_weight-old_weight,sign=1)
            else:
                self.update_macros(food, old_weight-new_weight,sign=1)
                self.update_days_macros_with_food(food, old_weight-new_weight,sign=1)
            meal[food] = new_weight


            print("Food weight changed successfully")
        else:
            print("Food does not exist")

    def add_food_to_meal(self, meal_number:int, food:str, weight:float):
        meal = self.meals[meal_number]
        if food in meal:
            print("Food already exists, please use change_food_weight() to change its weight")
            return 
        else:
            meal[food] = weight
            self.update_macros(food, weight,sign=1)