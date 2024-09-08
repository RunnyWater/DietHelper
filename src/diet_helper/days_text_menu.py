from .days import Days
from text_menu import DatabaseClassMenu

class DaysMenu(DatabaseClassMenu):

    def __init__(self, db_type:str, con_string:str=None, database_name:str=None ):
        super().__init__({
            1: 'add_meal',
            2: 'add_day',
            3: 'get_food',
            4: 'get_total_macros_by_date',
            5: 'get_meal_macros_by_date',
            6: 'get_all_meals_macros_by_date',
            'q': 'return'
        })
        print("Loading Days...")
        self.database:Days = Days(con_string=con_string, database_name=database_name, db_type=db_type)