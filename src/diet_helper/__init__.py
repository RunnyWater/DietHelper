# from .macro_helper import MacroManager
# from .diet_helper import FoodLister
from .foods import Foods
from .days import Days
import inspect
from config_manager import Config


_config = Config()
_database_type =int(_config.get('database', 'database_type'))


def set_database_name():
    user_input = input("\nPlease enter database name \nor 'q' to exit to main menu and change the database type to Local: ")
    if user_input.lower() == 'q':
        _config.set_database_option('database_type', '1')
        return 205
    else:
        database_name = user_input
        _config.set_database_option('database_name', database_name)
        return 200

def set_connection_string():
    user_input = input("\nPlease enter connection string \nor 'q' to exit to main menu and change the database type to Local: ")
    if user_input.lower() == 'q':
        _config.set_database_option('database_type', '1')
        return 205
    else:
        con_string = user_input
        _config.set_database_option('con_string', con_string)
        return 200

    

class TextMenu:
    def __init__(self, options:dict) -> None:
        self.options = options

    def run(self) -> None:
        self.handle_user_input(self.options)

    def handle_user_input(self, options:dict) -> None:
        while True:
            print("\nPlease select an option:")
            for key, value in options.items():
                print(f"{key}: {value}")
            choice:str = input("Enter the number of your choice: ")

            if choice.lower() == 'q':
                print("Exiting...")
                break

            try:
                # Convert choice to an integer if it's a valid option
                if choice.isdigit():
                    choice = int(choice)
                func_name:str = options[choice]
                
                # Get the function reference
                func = getattr(self.database, func_name)
                
                # Get the function signature to see if it requires arguments
                signature:inspect.Signature = inspect.signature(func)
                params:inspect.Parameter = signature.parameters

                # Check if the function requires arguments
                if params:
                    # Ask user to provide arguments
                    args:list = []
                    kwargs:dict = {}
                    for name, param in params.items():
                        if param.default == inspect.Parameter.empty:
                            value:str = input(f"Enter the value for '{name}': ")
                            args.append(value)
                        else:
                            value:str = input(f"'{name}' (Leave blank to use '{param.default}' value): ")
                            if value:
                                kwargs[name] = value

                    # Call the function with the collected arguments
                    result = func(*args, **kwargs)
                else:
                    # Call the function without arguments
                    result = func()                
                
            except KeyError:
                print("Invalid option. Please choose a valid number.")
            except AttributeError:
                print("Function not found. Please choose a valid option.")
            except TypeError as e:
                print(f"Argument error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")


class MainMenu(TextMenu):
    def __init__(self) -> None:
        super().__init__({1: 'days', 2: 'foods', 3: 'change_database_type', 'q': 'exit'})
        self.str_db_type = None
        self.con_string=None
        self.database_name=None
        self.get_database_attributes()
        self.database_menu = DatabaseMenu()
        self.days_menu = None
        self.foods_menu = None
        self.food_db_needs_reconnection = False
        self.days_db_needs_reconnection = False
        
        
    def connect_to_days_database(self):
        if self.days_menu == None or self.days_db_needs_reconnection:
            if self.str_db_type == 'mongo':
                if self.con_string is None:
                    if set_connection_string() == 205:
                        return
                if self.database_name is None:
                    if set_database_name() == 205:
                        return
            self.days_menu = DaysMenu(con_string=self.con_string, database_name=self.database_name, db_type=self.str_db_type)
            self.days_db_needs_reconnection = False

    def connect_to_foods_database(self):
        if self.foods_menu == None or self.food_db_needs_reconnection:
            if self.str_db_type == 'mongo':
                if self.con_string is None:
                    if set_connection_string() == 205:
                        return
                if self.database_name is None:
                    if set_database_name() == 205:
                        return
            self.foods_menu = FoodsMenu(con_string=self.con_string, database_name=self.database_name, db_type=self.str_db_type)
            self.food_db_needs_reconnection = False

    def get_database_attributes(self) -> None:
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


    # override of the parent function due to options linking to the classes itself and that requires another handling method
    def handle_user_input(self, *args) -> None:
        while True:
            print("\nPlease select an option:")
            for key, value in self.options.items():
                print(f"{key}: {value}")
            choice:str = input("Enter the number of your choice: ")

            if choice.lower() == 'q':
                print("Exiting...")
                break

            try:
                # Convert choice to an integer if it's a valid option
                if choice.isdigit():
                    choice = int(choice)
                
                if choice == 1:
                    self.days()
                elif choice == 2:
                    self.foods()
                elif choice == 3:
                    self.change_database_type()
                else:
                    print("Invalid option. Please choose a valid number.")
                
                
            except KeyError:
                print("Invalid option. Please choose a valid number.")
            except AttributeError:
                print("Function not found. Please choose a valid option.")
            except TypeError as e:
                print(f"Argument error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    def change_database_type(self):
        old_database_type =  _database_type
        self.database_menu.run()
        if old_database_type != _database_type:
            self.get_database_attributes()

    def days(self):
        self.connect_to_days_database()
        self.days_menu.run()

    def foods(self):
        self.connect_to_foods_database()
        self.foods_menu.run()

class DatabaseMenu(TextMenu):
    def __init__(self):
        self.array_options = ['Local', 'MongoDB']
        self.options:dict = {}
        self.update_option_dictionary()
        self.options[_database_type] += ' (Selected)'

    def update_option_dictionary(self):
        self.options = {}
        for key, value in enumerate(self.array_options):
            self.options[key+1] = value
        self.options['q'] = 'return'


    def handle_user_input(self, *args) -> None:
        while True:
            print("\nPlease select an option:")
            for key, value in self.options.items():
                print(f"{key}: {value}")
            choice:str = input("Enter the number of your choice: ")

            if choice.lower() == 'q':
                print("Exiting...")
                break

            elif choice.isdigit() and int(choice) in self.options:
                self.change_database_type(int(choice))

    def change_database_type(self, option):
        global _database_type
        _config.set_database_option('database_type', str(option))
        _database_type = int(option)
        self.update_option_dictionary()
        self.options[option] += ' (Selected)'


class DaysMenu(TextMenu):

    def __init__(self, con_string:str, database_name:str, db_type:str):
        # TODO: add possibility to use full options 
        # self.options = {1 :'add_meal', 2 :'add_day', 3 :'get_total_macros_by_date', 4 :'get_meal_macros_by_date', 5 :'get_all_meals_macros_by_date', 6 :'exit'}
        self.options:dict = {
            1: 'add_meal',
            2: 'add_day',
            3: 'get_food',
            4: 'get_total_macros_by_date',
            5: 'get_meal_macros_by_date',
            6: 'get_all_meals_macros_by_date',
            'q': 'return'
        }       
        print("Loading Days...")
        self.database:Days = Days(con_string=con_string, database_name=database_name, db_type=db_type)


class FoodsMenu(TextMenu):

    def __init__(self, con_string:str, database_name:str, db_type:str):
        # TODO: add possibility to use full options 
        # self.options = {1 :'add_food', 2 :'add_variant', 3 :'delete_food', 4 :'delete_variant', 5 :'get_foods', 'q' :'exit'}
        self.options:dict = {
            1 :'add_food', 
            2 :'add_variant', 
            3 :'delete_food',
            4 :'delete_variant', 
            5 :'get_foods',
            6 :'get_food',
            'q' :'return'}
        print("Loading Foods...")
        self.database:Foods= Foods(con_string=con_string, database_name=database_name, db_type=db_type)