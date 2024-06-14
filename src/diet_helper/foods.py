from .food_database import MongoManager
from .food_database import JsonManager
from .food import Food

class Foods:
    def __init__(self, con_string=None, database_name=None, food_collection_name=None, db_type='json'):
        if db_type == 'mongo':
            self.__manager = MongoManager(con_string, database_name, food_collection_name)
            self.foods = self.get_foods_mongo()
        else:
            self.__manager = JsonManager()
            self.foods =self.get_foods_json()
        if self.foods is None:
            exit('There was an error while gettting foods')


    def get_foods_mongo(self):
        food_list = self.__manager.get_foods()
        try: 
            foods = {}
            for food in food_list:
                foods[food['name'].lower()] = Food(name=food['name'], p=food['p'], f=food['f'], c=food['c'], variants=food['variants'])
            return foods
        except Exception as e:
            print( "There was an error while getting foods: " + str(e))
            return None
        

    def get_foods_json(self):
        return self.__manager.get_foods()


    def add_food(self, name, p, f, c, variants=None):
        name = name.lower()
        if name in self.get_names():
            return f"{name} already exists in database"
        self.foods[name] = Food(name=name, p=p, f=f, c=c)
        self.__manager.insert_food(name, p, f, c)
        if variants is not None:
            self.add_variant(name, variants)
        return f"{name} added to database with p: {p}, f: {f}, c: {c}"

    def add_variant(self, name, new_variant):
        name = name.lower()
        if self.__manager.add_variant(name, new_variant) == "Variant is not correct, please check it again": 
            return "Variant is not correct, please check it again"
        self.foods[name].add_variant(new_variant)
        return f"{name} updated"
    
    def update_food(self, name, p=None, f=None, c=None, variants=None):
        name = name.lower()
        self.foods[name].updateInfo(p, f, c, variants)
        self.__manager.update_food(name, p, f, c, variants)
        return f"{name} updated"

    def get_names(self):
        return list(self.foods.keys())

    def __repr__(self) -> str:
        return f"{self.foods}"
    

    def __getitem__(self, key):
        return self.foods[key]