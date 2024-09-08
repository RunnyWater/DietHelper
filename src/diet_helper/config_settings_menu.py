from text_menu import Menu
from .config_manager import Config


class ConfigSettingsMenu(Menu):
    def __init__(self, config:Config) -> None:
        super().__init__({
            1:'change_connection_string', 
            2:'change_database_name', 
            3:'change_user_name', 
            'q':'return'})
        self.config = config
        

    def change_setting(self, setting:str):
        user_input = input(f"Enter new {setting} or 'q' to exit:\n")
        if user_input.lower() != 'q':
            if input(f"Are you sure you want to change the {setting}? (y/n)\n").lower() == 'y':
                return user_input

        return None
    

    def change_connection_string(self):
        value = self.change_setting('connection string') 
        if value != None:
            self.config.set_database_option('connection_string', value)

        
    
    def change_database_name(self):
        value = self.change_setting('database name') 
        if value != None:
            self.config.set_database_option('database_name', value)

    
    def change_user_name(self):
        value = self.change_setting('user name') 
        if value != None:
            self.config.set_user_name(value)


class DatabaseChoiceMenu():
    def __init__(self, config:Config) -> None:
        self.config = config
        self.database_type = int(self.config.get('database', 'database_type'))
        self.array_options = ['Local', 'MongoDB']
        self.options:dict = {}
        self.update_option_dictionary()
        self.options[self.database_type] += ' (Selected)'

    def run(self):
        self.handle_user_input()
        return self.database_type

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
        self.config.set_database_option('database_type', str(option))
        self.database_type = int(option)
        self.update_option_dictionary()
        self.options[option] += ' (Selected)'