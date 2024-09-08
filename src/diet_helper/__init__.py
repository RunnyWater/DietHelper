from .config_manager import Config, urgent_set_connection_string, urgent_set_database_name
from .days_text_menu import DaysMenu
from .foods_text_menu import FoodsMenu
from .config_settings_menu import DatabaseChoiceMenu, ConfigSettingsMenu
from text_menu import Menu

_config = Config()
_database_type = _database_type =int(_config.get('database', 'database_type'))

def is_mongo_info_given(con_string, database_name) -> bool:
    if con_string is None:
        if urgent_set_connection_string(_config) == 205:
            return False
    if database_name is None:
        if urgent_set_database_name(_config) == 205:
            return False
    return True
    

class MainMenu(Menu):
    def __init__(self) -> None:
        super().__init__({1: 'days', 2: 'foods', 3: 'change_database_type', 4: 'config_settings', 'q': 'exit'})
        self.str_db_type = None
        self.con_string=None
        self.database_name=None
        self.get_database_attributes()
        self.database_menu = DatabaseChoiceMenu(_config)
        self.config_settings_menu = ConfigSettingsMenu(_config)
        self.days_menu = None
        self.foods_menu = None
        self.food_db_needs_reconnection = False
        self.days_db_needs_reconnection = False
        
        
    def run(self) -> None:
        print(f'Hello, {_config.get('user', 'user_name')}!')
        print('Welcome to Diet Helper!')
        self.handle_user_input(self.options)


    def connect_to_days_database(self):
        if self.days_menu == None or self.days_db_needs_reconnection:
            if self.str_db_type == 'mongo':
                if is_mongo_info_given(self.con_string, self.database_name):
                    self.days_menu = DaysMenu(con_string=self.con_string, database_name=self.database_name, db_type=self.str_db_type)
                    self.days_db_needs_reconnection = False
                else:
                    return
            else:
                self.days_menu = DaysMenu(db_type=self.str_db_type)
                self.days_db_needs_reconnection = False


    def connect_to_foods_database(self):
        if self.foods_menu == None or self.food_db_needs_reconnection:
            if self.str_db_type == 'mongo':
                if is_mongo_info_given(self.con_string, self.database_name):
                    self.foods_menu = FoodsMenu(con_string=self.con_string, database_name=self.database_name, db_type=self.str_db_type)
                    self.food_db_needs_reconnection = False
                else:
                    return
            else:
                self.foods_menu = FoodsMenu(db_type=self.str_db_type)
                self.food_db_needs_reconnection = False


    def get_database_attributes(self) -> None:
        try :
            print("Connecting to databases...")
            if _database_type == 1:
                if self.str_db_type == 'mongo':
                    self.food_db_needs_reconnection = True
                    self.days_db_needs_reconnection = True
                self.str_db_type = 'json'
                self.con_string=None
                self.database_name=None
            elif _database_type == 2:
                if self.str_db_type == 'json':
                    self.food_db_needs_reconnection = True
                    self.days_db_needs_reconnection = True
                self.str_db_type = 'mongo'
                self.con_string=_config.get('database', 'con_string')
                self.database_name=_config.get('database', 'database_name')
        except Exception as e:
            print(e)

    def days(self):
        self.connect_to_days_database()
        self.days_menu.run()

    def foods(self):
        self.connect_to_foods_database()
        self.foods_menu.run()

    def change_database_type(self):
        global _database_type
        old_database_type =  _database_type
        _database_type = self.database_menu.run()
        if old_database_type != _database_type:
            self.get_database_attributes()

    def config_settings(self):
        self.config_settings_menu.run()

