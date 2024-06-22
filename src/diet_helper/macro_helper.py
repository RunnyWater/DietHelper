from .calculator import * 

class MacroManager:

    def __init__(self, foods):
        self.foods = foods

    def get_info_with_variant(self, food_name:str, variant_name:dict=None, info_calories:bool=False, info_protein:bool=False, info_fat:bool=False, info_carbs:bool=False) -> int:
        try:
            food = self.foods[food_name.lower()]
            vars = food.variants.keys()
            if variant_name == None or vars == None or vars == []:
                variant_name = input(', '.join(food.variants.keys())+' please choose one of these variants: ')
        except Exception as e:
            return "There was an error while searching food: " + str(e)
        
        try:
            str_weight =food.variants[variant_name.lower()]
            weight = int(str_weight) / 100.0
        except KeyError as e:
            return("This variant was not found: " + str(e)+'\n' +food_name+ 'has no such variant: , '.join(food.variants.keys()))
        except Exception as e:
            return "There was an error while searching and processing food's variant: " + str(e)
        return self.get_info_with_grams(food_name, weight, get_calories_boolean=info_calories, get_protein_boolean=info_protein, get_fat_boolean=info_fat, get_carbs_boolean=info_carbs)


    def get_info_with_grams(self, food_name:str, weight:int=100, get_calories_boolean:bool=False, get_protein_boolean:bool=False, get_fat_boolean:bool=False, get_carbs_boolean:bool=False) -> int:
        food = self.foods[food_name.lower()]
        info = {}
        weight=weight/100
        if get_calories_boolean:
            info['calories'] = get_calories(weight, p=food.proteins, f=food.fats, c=food.carbs)
        if get_protein_boolean:
            info['protein']=get_proteins(weight, p=food.proteins)
        if get_fat_boolean:
            info['fat'] =get_fats(weight, f=food.fats)
        if get_carbs_boolean:
            info['carbs']=get_carbs(weight, c=food.carbs)
        return info



    