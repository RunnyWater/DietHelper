from .macro_helper import MacroManager

class FoodLister:
    def __init__(self, food_collection):
        self.food_collection = food_collection

    # list all food, that have 10 or less calories per 1 protein
    # this is a good practice for dieting
    def list_best_protein_per_calorie_foods(self) -> dict:
        foods = self.food_collection.find()
        best_food = {}
        macro_manager = MacroManager(self.food_collection)
        for food in foods:
            info = macro_manager.get_info_with_weight(food_name=food['name'], get_calories=True, get_protein=True)
            protein = int(info['protein'])
            calories = int(info['calories'])
            calories_per_protein_ration = round(calories/protein,1)
            if calories_per_protein_ration<=10:
                best_food.update({food['name']: {'protein':protein, 'calories':calories, 'calories_per_protein_ration':calories_per_protein_ration}})
        if len(best_food) > 0:
            return best_food
        return "No food has calories per protein ration less than 10"