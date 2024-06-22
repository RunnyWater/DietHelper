from .food_database import MongoFoodManager
from .food_database import JsonFoodManager
from .food import Food

class Foods:
    def __init__(self, con_string=None, database_name=None, food_collection_name='food', db_type='json', json_file_path='json/foods.json'):
        if db_type == 'mongo':
            self.__manager = MongoFoodManager(con_string, database_name, food_collection_name)
            self.foods = self.get_foods_mongo()
        else:
            self.__manager = JsonFoodManager(json_file_path)
            self.foods =self.get_foods_json()
        if self.foods is None:
            exit('There was an error while gettting foods from database')


    def get_foods_mongo(self):
        food_list = self.__manager.get_foods()
        try: 
            foods = {}
            for food in food_list:
                foods[food['name'].lower()] = Food(name=food['name'], p=food['p'], f=food['f'], c=food['c'], variants=food['variants'])
            self.__manager.close_connection()
            return foods
        except Exception as e:
            print( "There was an error while getting foods: " + str(e))
            return None
        

    def get_foods_json(self):
        return self.__manager.get_foods()


    def add_food(self, name:str, p:int, f:int, c:int, variants=None):
        name = name.lower()
        if name in self.get_names():
            return f"{name} already exists in database"
        self.foods[name] = Food(name=name, p=p, f=f, c=c)
        self.__manager.insert_food(name, p, f, c)
        if variants is not None:
            self.add_variant(name, variants)
        return f"{name} added to database with p: {p}, f: {f}, c: {c}"

    def add_variant(self, name:str, new_variant:dict):
        name = name.lower()
        if self.__manager.add_variant(name, new_variant) == "Variant is not correct, please check it again": 
            return "Variant is not correct, please check it again"
        self.foods[name].add_variant(new_variant)
        return f"{name} updated"

    def update_variant(self, name:str, variant_name:str, new_value:int):
        name = name.lower()
        if self.foods[name].update_variant(variant_name, new_value) == '404': 
            return 'Error code: 404'
        self.__manager.update_variant(name, variant_name, new_value)
        return f"{name}, {variant_name} updated to {new_value}"

    def delete_variant(self, name:str, variant_name:str):
        name = name.lower()
        self.foods[name].delete_variant(variant_name)
        self.__manager.delete_variant(name, variant_name)
        return f"{name}, variant {variant_name} deleted"

    def update_food(self, name:str, p:int=None, f:int=None, c:int=None, variants:dict=None):
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