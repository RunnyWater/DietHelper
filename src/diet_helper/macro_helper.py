
class MacroManager:

    def __init__(self, foods):
        self.foods = foods

    def get_info_with_variant(self, food_name=str, variant=None, get_calories=False, get_protein=False, get_fat=False, get_carbs=False) -> int:
        try:
            food = self.foods[food_name.lower()]
            vars = food.variants.keys()
            if variant == None or vars == None or vars == []:
                variant = input(', '.join(food.variants.keys())+' please choose one of these variants: ')
        except Exception as e:
            return "There was an error while searching food: " + str(e)
        
        try:
            str_weight =food.variants[variant.lower()]
            weight = int(str_weight) / 100.0
        except KeyError as e:
            return("This variant was not found: " + str(e)+'\n' +food_name+ 'has no such variant: , '.join(food.variants.keys()))
        except Exception as e:
            return "There was an error while searching and processing food's variant: " + str(e)
        info = {}
        if get_calories:
            info['calories'] = food.get_calories(weight)
        if get_protein:
            info['protein']=food.get_proteins(weight)
        if get_fat:
            info['fat'] =food.get_fats(weight)
        if get_carbs:
            info['carbs']=food.get_carbs(weight)
        return info


    def get_info_with_weight(self, food_name=str, weight=100, get_calories=False, get_protein=False, get_fat=False, get_carbs=False) -> int:
        food = self.foods[food_name.lower()]
        info = {}
        weight=weight/100
        if get_calories:
            info['calories'] = food.get_calories(weight)
        if get_protein:
            info['protein']=food.get_proteins(weight)
        if get_fat:
            info['fat'] =food.get_fats(weight)
        if get_carbs:
            info['carbs']=food.get_carbs(weight)
        return info



    