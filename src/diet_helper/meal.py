class Meal:
    def __init__(self, food_collection):
        self.food_collection = food_collection
        self.foods = {}
        self.sum_of_proteins = 0
        self.sum_of_fats = 0
        self.sum_of_carbs = 0
        self.sum_of_calories = 0
        self.note = '' # TODO: add note functionality

    def add_food(self, food_name, weight):
        try:
            food = self.food_collection[food_name]
        except KeyError as e:
            return "There was an error while searching food: " + str(e)
        if food_name in self.foods:
            if input( "This food is already in meal, do you want to update its weight? (y/n)") == 'y':
               return self.update_weight(food_name, weight)
            elif input("Do you want to add another food? (y/n)") == 'n':
                return f"{food_name} already in the meal"
        self.foods[food_name] = {food.name: weight}
        self.update_macros(food_name, weight)
        return f"{food_name} added to meal with weight {weight}"
    

    def update_weight(self, food_name, new_weight):
        old_weight = self.get_weight(food_name)
        difference = round(new_weight - old_weight, 2)
        self.update_macros(food_name, difference)
        self.set_weight(food_name, new_weight)
        return f"Weight of {food_name} updated from {old_weight} to {new_weight}"


    def delete_food(self, food_name):
        old_weight = self.get_weight(food_name)
        del self.foods[food_name]
        self.update_macros(food_name, old_weight, -1)
        return f"{food_name} deleted from meal"


    def get_weight(self, food_name):
        return float(self.foods[food_name][food_name])


    def set_weight(self, food_name, new_weight):
        self.foods[food_name][food_name] = new_weight
        return f"Weight of {food_name} updated to {new_weight}"
        

    def update_macros(self, food_name, weight, sign=1):
        self.sum_of_proteins += self.food_collection[food_name].get_proteins(weight*sign)
        self.sum_of_fats +=     self.food_collection[food_name].get_fats(weight*sign)
        self.sum_of_carbs +=    self.food_collection[food_name].get_carbs(weight*sign)
        self.sum_of_calories += self.food_collection[food_name].get_calories(weight*sign)


    def get_foods(self):
        return list(self.foods.keys())


    def __repr__(self) -> str:
        return f"{self.foods}"


    def __str__(self) -> str:
        return f"Sum of proteins: {self.sum_of_proteins}g\nSum of fats: {self.sum_of_fats}g\nSum of carbs: {self.sum_of_carbs}g\nSum of calories: {self.sum_of_calories}kcal"
    
