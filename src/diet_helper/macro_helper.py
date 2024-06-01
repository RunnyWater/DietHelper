
class MacroManager:

    def __init__(self, food_collection):
        self.food_collection = food_collection

    def get_info_with_variant(self, food_name=str, variant=None, get_calories=False, get_protein=False, get_fat=False, get_carbs=False) -> int:
        try:
            food = self.food_collection.find_one({"name":food_name.lower()})
            if variant == None:
                variant = input(', '.join(food['variants'].keys())+' please choose one of these variants: ')
        except Exception as e:
            return "There was an error while searching food: " + str(e)
        
        try:
            str_weight =food['variants'][variant.lower()]
            weight = int(str_weight) / 100.0
        except KeyError as e:
            return("This variant was not found: " + str(e)+'\n' +food_name+ 'has no such variant: , '.join(food['variants'].keys()))
        except Exception as e:
            return "There was an error while searching and processing food's variant: " + str(e)
        info = {}
        if get_calories:
            info['calories'] = round((int(food['p']) * 4 + int(food['f']) * 9 + int( food['c'])*4) * weight, 2)
        if get_protein:
            info['protein']=round( int(food['p']) * weight, 2)
        if get_fat:
            info['fat'] =round( int(food['f']) * weight,2)
        if get_carbs:
            info['carbs']=round( int( food['c']) * weight,2)
        return info


    def get_info_with_weight(self, food_name=str, weight=1, get_calories=False, get_protein=False, get_fat=False, get_carbs=False) -> int:
        food = self.food_collection.find_one({"name":food_name.lower()})
        info = {}
        if get_calories:
            info['calories'] = round((int(food['p']) * 4 + int(food['f']) * 9 + int( food['c'])*4) * weight, 2)
        if get_protein:
            info['protein']=round( int(food['p']) * weight, 2)
        if get_fat:
            info['fat'] =round( int(food['f']) * weight,2)
        if get_carbs:
            info['carbs']=round( int( food['c']) * weight,2)
        
        return info


    