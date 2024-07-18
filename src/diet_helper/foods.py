from .food_database import MongoFoodManager
from .food_database import JsonFoodManager
from .calculator import * 

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


    def add_food(self, name:str, p:int, f:int, c:int, variants=None, print_stages: bool = False):
        name = name.lower()
        if name in self.get_names():
            print( f"{name} already exists in database")
            return
        self.foods[name] = Food(name=name, p=p, f=f, c=c)
        self.__manager.insert_food(name, p, f, c)
        if variants is not None:
            self.add_variant(name, variants)
        if print_stages: print( f"{name} added to database with p: {p}, f: {f}, c: {c}")

    def add_variant(self, name:str, new_variant:dict, print_stages: bool = False):
        name = name.lower()
        if self.__manager.add_variant(name, new_variant) == "Variant is not correct, please check it again": 
            print(  "Variant is not correct, please check it again")
        self.foods[name].add_variant(new_variant)
        if print_stages: print( f"{name} updated")

    def update_variant(self, name:str, variant_name:str, new_value:int, print_stages: bool = False):
        name = name.lower()
        if self.foods[name].update_variant(variant_name, new_value) == '404': 
            print(  'Error code: 404')
        self.__manager.update_variant(name, variant_name, new_value)
        if print_stages: print( f"{name}, {variant_name} updated to {new_value}")

    def delete_variant(self, name:str, variant_name:str, print_stages: bool = False):
        name = name.lower()
        self.foods[name].delete_variant(variant_name)
        self.__manager.delete_variant(name, variant_name)
        if print_stages: print( f"{name}, variant {variant_name} deleted")

    def update_food(self, name:str, p:int=None, f:int=None, c:int=None, variants:dict=None, print_stages: bool = False):
        name = name.lower()
        self.foods[name].updateInfo(p, f, c, variants)
        self.__manager.update_food(name, p, f, c, variants)
        if print_stages: print( f"{name} updated")

    def get_macros_by_name(self, name:str):
        name = name.lower()
        return self.foods[name].get_macros()

    def get_names(self):
        return list(self.foods.keys())

    def __repr__(self) -> str:
        return f"{self.foods}"
    

    def __getitem__(self, key):
        return self.foods[key]
    

class Food:
    def __init__(self, name, p, f, c, variants=None):
        self.name = str(name)
        self.proteins = int(p)
        self.fats = int(f)
        self.carbs = int(c)
        self.variants = variants

    def update_info(self, name:str, p:int, f:int, c:int, variants:dict = None, print_stages: bool = False) -> str:
        if name is not None:
            self.name = name
        if p is not None:
            self.proteins = p
        if f is not None:
            self.fats = f
        if c is not None:
            self.carbs = c
        if variants is not None:
            self.variants = {}
        if print_stages: print( f'{self.name} updated')
    

    def add_variant(self, new_variant:dict, print_stages: bool = False) -> str:
        if self.variants is None:
            self.variants = {}
        self.variants.update(new_variant)
        if print_stages: print( f"{', '.join(new_variant.keys())} added to {self.name}")


    def update_variant(self, variant_name:str, new_weight:int, print_stages: bool = False) -> str:
        if self.variants is None or variant_name not in list(self.variants.keys()):
            print( f"{self.name} has no variant with name {variant_name}\nPlease choose out of the following: {', '.join(self.variants.keys())}")
            return
        self.variants[variant_name] = new_weight
        if print_stages: print( f"variant {self.name} now has {new_weight}")
    

    def delete_variant(self, variant_name:str, print_stages: bool = False):
        if self.variants is None:
            print(  f"food `{self.name}` has no variants")
        del self.variants[variant_name]
        if len(self.variants) == 0:
            self.variants = None
            print(  f"food `{self.name}` has no variants")
        if print_stages: print( f"variant {self.name} now has {self.variants}")


    def get_info_for_json(self):
        food_dict = {
            "name": self.name,
            "p": self.proteins,
            "f": self.fats,
            "c": self.carbs,
            "variants": self.variants
        }
        return food_dict

    def get_name(self) -> str:
        return self.name
    
    def get_macros(self) -> dict:
        return {
            "p": self.proteins,
            "f": self.fats,
            "c": self.carbs,
            "cal": self.proteins * 4 + self.fats * 9 + self.carbs * 4
        }

    def __repr__(self) -> str:
        return f"Food(name={self.name}, proteins={self.proteins}, fats={self.fats}, carbs={self.carbs}, variants={self.variants})"
    
    def __str__(self) -> str:
        return f'{self.name} per 100g: {self.proteins}g of proteins, {self.fats}g of fats, {self.carbs}g of carbs'