from .macro_helper import MacroManager
from .diet_helper import FoodLister
from .foods import Foods
from .days import Days
import inspect

class TextMenu:
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
                    
                print("Function executed successfully. Result:", result)
                
                
            except KeyError:
                print("Invalid option. Please choose a valid number.")
            except AttributeError:
                print("Function not found. Please choose a valid option.")
            except TypeError as e:
                print(f"Argument error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

class DaysMenu(TextMenu):

    def __init__(self):
        
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
        self.database:Days = Days()
        self.handle_user_input(self.options)

class FoodsMenu(TextMenu):

    def __init__(self):
        
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
        self.database:Foods= Foods()

        self.handle_user_input(self.options)

class MainMenu(TextMenu):
    def __init__(self) -> None:
        self.options = {1: 'days', 2: 'foods', 3: 'change_database_type', 'q': 'exit'}
        self.days_menu = DaysMenu()
        self.foods_menu = FoodsMenu()
        self.handle_user_input()
        all_members = inspect.getmembers(self)

        # Filter to include only functions
        functions = [member[0] for member in all_members if inspect.isfunction(member[1])]

    # override of the parent function due to options linking to the classes itself and that requires another handling method
    def handle_user_input(self) -> None:
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
                func_name:str = self.options[choice]
                
                func = getattr(self, func_name)

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
                    
                print("Function executed successfully. Result:", result)
                
                
            except KeyError:
                print("Invalid option. Please choose a valid number.")
            except AttributeError:
                print("Function not found. Please choose a valid option.")
            except TypeError as e:
                print(f"Argument error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")


    def change_database_type(self):
        pass

    def days(self):
        pass

    def foods(self):
        pass