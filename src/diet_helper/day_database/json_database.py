import os
import json 
from datetime import datetime, timedelta

def get_start_of_the_day(day:datetime | str):
    if isinstance(day, str):
        day = datetime.strptime(day, '%Y-%m-%d')
    return datetime.combine(day, datetime.min.time())

def from_string_to_date(date:str | datetime):
    if isinstance(date, str):
        return datetime.strptime(date, '%Y-%m-%d')
    else:
        return get_start_of_the_day(date)

def get_todays_date():
    return datetime.combine(datetime.today(), datetime.min.time())

class JsonDayManager:
    def __init__(self, json_file_path='json/days.json'):
        self.json_path = self.get_database(json_file_path)
        self.data = self.load()


    def get_database(self, json_file_path='json/days.json'):
        try:
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
            with open(json_file_path, 'r') as f:
                return json_file_path
                
        except FileExistsError:
            try:
                with open(json_file_path, 'r') as f:
                    if f.read() != '':
                        return json_file_path
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            return json_file_path


    def get_days(self):
        return self.data


    def get_day(self, date:datetime | str):
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date = get_start_of_the_day(date)
        date = str(date)
        if date in self.data:
            return self.data[date]
        else:
            return "There is no such day in database"
        

    def load(self):
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        


    def save(self):
        old_data = self.load()
        try: 
            with open(self.json_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"An unexpected error occurred during saving data: {e}")
            with open(self.json_path, 'w') as f:
                json.dump(old_data, f, indent=4)

    def get_days_by_month(self, month:int = datetime.now().month, year:int = datetime.now().year):
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        days = self.get_days_between_two_dates(start_date, end_date)
        return days
    
    def get_days_between_two_dates(self, start_date:datetime, end_date:datetime):  
        if isinstance(start_date, str):
            start_date = from_string_to_date(start_date)
        if isinstance(end_date, str):
            end_date = from_string_to_date(end_date)
        try:
            days = {date:self.data[date] for date in self.data.keys() if start_date <= from_string_to_date(date) <= end_date}
            return days
        except Exception as e:
            print( "There was an error while getting days: " + str(e))
            return None


    def add_day(self, day:datetime | str = None, meals:list[dict] = [], print_stages: bool = False):
        if day is None:
            date = get_start_of_the_day(get_todays_date())
        else: 
            date = get_start_of_the_day(day)
        if isinstance(date, datetime):
            date = str(date)
            
        if date in self.data.keys():
            print("Day already exists")
            return 
        else: 
            self.data[date] = {"meals":meals}
            self.save()
            if print_stages: print("Day added successfully")
            return
        

    def add_meal(self, day:datetime | str = None, meal:dict = {}, print_stages: bool = False):
        if day is None:
            date = get_start_of_the_day(get_todays_date())
        else:
            date = get_start_of_the_day(day)
        if isinstance(date, datetime):
            date = str(date)
        if date not in self.data.keys():
            print("Day does not exist")
            return
        try:
            self.data[date]["meals"].append(meal) # pushing meal to day's meals list
            self.save()
            if print_stages: print("Meal added successfully to day")
            return 
        except Exception as e:
            print( "There was an error while adding meal: " + str(e))
            return 
        
    def add_food_to_day(self, day:datetime | str, meal_number:int, food:str, weight:float, print_stages: bool = False):
        meal_number = meal_number - 1
        date = get_start_of_the_day(day)
        if isinstance(date, datetime):
                    date = str(date)
        if date not in self.data.keys():
            print("Day does not exist")
            return
        try:
            if len(self.data[date]["meals"]) < meal_number + 1:
                print("Meal does not exist")
                return
            else:
                if food in self.data[date]["meals"][meal_number].keys():
                    print("Food already exists")
                    return 
                else:
                    self.data[date]["meals"][meal_number][food] = weight
                    self.save()
                    if print_stages: print("Food added successfully to meal")
                    return None
        except Exception as e:
            self.close_connection()
            print( "There was an error while adding food: " + str(e))
            return 404
    
    def change_food_weigth_in_meal(self, day:datetime, meal_number:int, food:str, weight:float, print_stages: bool = False):
        meal_number = meal_number - 1
        date =  get_start_of_the_day(day)
        if isinstance(date, datetime):
                    date = str(date)
        if date not in self.data.keys():
            print("Day does not exist")
            return
        try:
            if len(self.data[date]["meals"]) < meal_number + 1:
                print("Meal does not exist")
                return
            else:
                if food not in self.data[date]["meals"][meal_number].keys():
                    print("Food does not exists")
                    return 
                else:
                    self.data[date]["meals"][meal_number][food] = weight
                    self.save()
                    if print_stages: print("Food added successfully to meal")
                    return None
        except Exception as e:
            self.close_connection()
            print( "There was an error while adding food: " + str(e))
            return 404

    def delete_food_from_meal(self, day:datetime, meal_number:int, food:str, print_stages: bool = False):
        meal_number = meal_number - 1
        date =  get_start_of_the_day(day)
        if isinstance(date, datetime):
                    date = str(date)
        if date not in self.data.keys():
            print("Day does not exist")
            return
        try:
            if len(self.data[date]["meals"]) < meal_number + 1:
                print("Meal does not exist")
                return
            else:
                if food not in self.data[date]["meals"][meal_number].keys():
                    print("Food does not exists")
                    return 
                else:
                    del self.data[date]["meals"][meal_number][food]
                    self.save()
                    if print_stages: print("Food added successfully to meal")
                    return None
        except Exception as e:
            self.close_connection()
            print( "There was an error while adding food: " + str(e))
            return 404
        