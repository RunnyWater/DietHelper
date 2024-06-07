from .macro_helper import MacroManager

class FoodLister:
    def __init__(self, foods):
        self.foods = foods

    # list all food, that have 10 or less calories per 1 protein
    # this is a good practice for dieting
    def list_best_protein_per_calorie_foods(self) -> dict:
        best_food = {}
        macro_manager = MacroManager(self.foods)
        for food_name in self.foods.getNames():
            info = macro_manager.get_info_with_weight(food_name=food_name, get_calories=True, get_protein=True)
            protein = int(info['protein'])
            calories = int(info['calories'])
            calories_per_protein_ration = round(calories/protein,1)
            if calories_per_protein_ration<=10:
                best_food.update({food_name: {'protein':protein, 'calories':calories, 'calories_per_protein_ration':calories_per_protein_ration}})
        if len(best_food) > 0:
            return best_food
        return "No food has calories per protein ration less than 10"