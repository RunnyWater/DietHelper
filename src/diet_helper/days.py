from .day_database import MongoDayManager
from .day import Day
from .meals import Meals

class Days:
    def __init__(self, con_string=None, database_name=None, day_collection_name='day', db_type='json', json_file_path='json/days.json'):
        self.meals = Meals(db_type=self.db_type, json_file_path=self.json_file_path)
        if db_type == 'mongo':
            self.__manager = MongoDayManager(con_string, database_name, day_collection_name)
            self.days = self.get_days_mongo()
        else:
            self.__manager = None
            # self.days = self.get_days_json()
        if self.days is None:
            exit('There was an error while gettting days from database')

    def get_days_mongo(self):
        days = {}
        for day in self.__manager.get_days():
            meal_ids = day['meals']
            days[day['_id']] = Day(meal_ids, day['_id'], db_type='mongo')
            if len(meal_ids)> 0:
                for meal_id in set(meal_ids):
                    if meal_id not in set(self.meals.meals.keys()):
                        exit('There was an error while gettting meal_ids from database')
                    macros = self.meals.get_meal_by_id(meal_id).get_macros()
                    p = macros['p']
                    f = macros['f']
                    c = macros['c']
                    cal = macros['cal']
                    days[day['_id']].update_macros(p, f, c, cal)
        return days 

    def get_days_json(self):
        # TODO: implement json
        return None
    
    def create_and_add_empty_meal(self, date):
        meal_id = self.meals.create_empty_meal(return_id=True)
        if meal_id not in set(self.meals.meals.keys()):
            return 404
        macros = self.meals.get_meal_by_id(meal_id).get_macros()
        self.days[date].add_meal(meal_id, macros)

    def add_meal(self, date, meal_id):
        if date not in self.days:
            print("Day does not exist")
            return 
        self.days[date].add_meal(meal_id)
        self.__manager.add_day(date, self.days[date].meal_ids)

    def delete_meal(self, date, meal_id):
        if date not in list(self.days.keys()):
            print("Day does not exist")
            return 
        macros = self.meals.get_meal_by_id(meal_id).get_macros()
        self.days[date].delete_meal(meal_id, macros)
        self.__manager.delete_day(date, meal_id)