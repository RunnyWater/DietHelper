import inspect

class Menu:
    def __init__(self, options : dict, menu_type : int = 0) -> None:
        self.options = options
        self.menu_type = menu_type

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
                if choice.isdigit() and int(choice) in options.keys():
                    choice = int(choice)
                func_name:str = options[choice]
                
                # Get the function reference
                if self.menu_type == 0:
                    func = getattr(self, func_name)
                elif self.menu_type == 1:
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



class DatabaseClassMenu(Menu):
    def __init__(self, options:dict) -> None:
        super().__init__(options, 1)
        
