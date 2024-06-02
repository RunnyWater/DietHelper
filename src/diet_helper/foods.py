from .mongo_database import MongoManager
from .json_database import JsonManager
from .macro_helper import MacroManager
from .diet_helper import FoodLister
from .food import Food

class Foods:
    def __init__(self, con_string, database_name, food_collection_name, db_type='json'):
        if db_type == 'mongo':
            self.manager = MongoManager(con_string, database_name, food_collection_name)
        else:
            self.manager = None # TODO: implement JsonManager
        self.foods =self.getFoods()

    def getFoods(self):
        mongo_list = self.manager.get_collection().find()
        try: 
            foods = {}
            for food in mongo_list:
                foods.update({food['name']: Food(name=food['name'], p=food['p'], f=food['f'], c=food['c'], variants=food['variants'])})
            
            self.manager.close_connection()
            return foods
        except Exception as e:
            self.manager.close_connection()
            return "There was an error while getting foods: " + str(e)
        

    def __repr__(self) -> str:
        return f"{self.foods}"