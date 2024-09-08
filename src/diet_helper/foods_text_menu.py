from .foods import Foods
from text_menu import DatabaseClassMenu

class FoodsMenu(DatabaseClassMenu):

    def __init__(self, db_type:str, con_string:str=None, database_name:str=None ):
        menu_dict = {
            1: 'add_food', 
            2: 'add_variant', 
            3: 'delete_food',
            4: 'delete_variant', 
            5: 'get_foods',
            6: 'get_food',
            'q': 'return'
        }
        super().__init__(menu_dict)
        print("Loading Foods...")
        self.database:Foods= Foods(con_string=con_string, database_name=database_name, db_type=db_type)
