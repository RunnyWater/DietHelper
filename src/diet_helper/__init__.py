from .macro_helper import MacroManager
from .diet_helper import FoodLister
from .foods import Foods
from .days import Days
import inspect

class TextMenu:
    def handle_user_input(self, options:dict):
        while True:
            print(self.options)
            print("\nPlease select an option:")
            for key, value in self.options.items():
                print(f"{key}: {value}")
            choice = input("Enter the number of your choice: ")

            if choice.lower() == 'q':
                print("Exiting...")
                break

            try:
                # Convert choice to an integer if it's a valid option
                if choice.isdigit():
                    choice = int(choice)
                func_name = self.options[choice]
                
                # Get the function reference
                func = getattr(self.days, func_name)
                
                # Get the function signature to see if it requires arguments
                signature = inspect.signature(func)
                params = signature.parameters

                # Check if the function requires arguments
                if params:
                    # Ask user to provide arguments
                    args = []
                    kwargs = {}
                    print(params.items())
                    for name, param in params.items():
                        if param.default == inspect.Parameter.empty:
                            value = input(f"Enter the value for '{name}': ")
                            args.append(value)
                        else:
                            value = input(f"'{name}' (Leave blank to use '{param.default}' value): ")
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
        self.options = {
            1: 'add_meal',
            2: 'add_day',
            3: 'get_food',
            4: 'get_total_macros_by_date',
            'q': 'return'
        }
        self.days = Days()

        self.text_menu = self.handle_user_input(self.options)

class FoodsMenu(TextMenu):

    def __init__(self):
        
        # TODO: add possibility to use full options 
        # self.options = {1 :'add_food', 2 :'add_variant', 3 :'delete_food', 4 :'delete_variant', 5 :'get_foods', 'q' :'exit'}
        self.options = {
            1 :'add_food', 
            2 :'add_variant', 
            3 :'delete_food',
            4 :'delete_variant', 
            5 :'get_foods',
            6 :'get_food',
            'q' :'return'}
        self.foods = Foods()

        self.text_menu = self.handle_user_input(self.options)