from .food_database import MongoManager
from .food_database import JsonManager
from .food import Food

class Foods:
    def __init__(self, con_string, database_name, food_collection_name, db_type='json'):
        if db_type == 'mongo':
            self.__manager = MongoManager(con_string, database_name, food_collection_name)
        else:
            self.__manager = None # TODO: implement JsonManager
        self.foods =self.getFoods()

    def getFoods(self):
        mongo_list = self.__manager.get_foods()
        try: 
            foods = {}
            for food in mongo_list:
                foods[food['name'].lower()] = Food(name=food['name'], p=food['p'], f=food['f'], c=food['c'], variants=food['variants'])
            self.__manager.close_connection()
            return foods
        except Exception as e:
            self.__manager.close_connection()
            return "There was an error while getting foods: " + str(e)

    def addFood(self, name, p, f, c, variants=None):
        self.foods[name] = Food(name=name, p=p, f=f, c=c)
        self.__manager.insert_food(name, p, f, c)
        if variants is not None:
            self.addVariant(name, variants)
        return f"{name} added to database with p: {p}, f: {f}, c: {c}"

    def addVariant(self, name, new_variant):
        if self.__manager.add_variant(name, new_variant) == "Variant is not correct, please check it again": 
            return "Variant is not correct, please check it again"
        self.foods[name].add_variant(new_variant)
        return f"{name} updated"
    
    def updateFood(self, name, p=None, f=None, c=None, variants=None):
        self.foods[name].updateInfo(p, f, c, variants)
        self.__manager.update_food(name, p, f, c, variants)
        return f"{name} updated"

    def getNames(self):
        return list(self.foods.keys())

    def __repr__(self) -> str:
        return f"{self.foods}"
    

    def __getitem__(self, key):
        return self.foods[key]