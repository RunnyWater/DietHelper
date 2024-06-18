class Meal:
    def __init__(self):
        self.foods = {}
        self.sum_of_proteins = 0
        self.sum_of_fats = 0
        self.sum_of_carbs = 0
        self.sum_of_calories = 0

    def add_food(self, food, weight):
        food_name = food.get_name()
        if food_name in list(self.foods.keys()):
            if input( "This food is already in meal, do you want to update its weight? (y/n)") == 'y':
               return self.update_weight(food_name, weight)
            elif input("Do you want to add another food? (y/n)") == 'n':
                return f"{food_name} already in the meal"
        self.foods[food_name] = [food, weight]
        self.update_macros(food_name, weight)
        return f"{food_name} added to meal with weight {weight}"

    '''
    Due to it leading to really big memory usage in the long run
    I do not recommend using note function:
     - FREE tier MongoDB
     - Limited memory on your server if you're using other database
     - notes with very long text
     If nevertheless you have a need for it, you can use it with note compression package''' # TODO: add connection to note managing package
    # def add_note(self, note):
    #     note = str(note)
    #     if self.note != '':
    #         input = ''
    #         while(input not in ['a', 'u', 'exit']):
    #             input = input("Do you want 'add to' or 'update' note? (a/u), or type 'exit' if you want to exit").lower()
    #         if input == 'u':
    #             self.note = note
    #         elif input == 'a':
    #             self.note = self.note + '\n' + note
    #     else:
    #         self.note = note
    #     return f"Note added to meal: {self.note}"

    
    # def dekete_note(self):
    #     if self.note != '':
    #         self.note = ''
    #         return f"Note deleted from meal"
    #     else:
    #         return f"No note in meal"
        

    # def get_note(self):
    #     return self.note


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
        return self.foods[food_name][1]


    def set_weight(self, food_name, new_weight):
        self.foods[food_name][1] = new_weight
        return f"Weight of {food_name} updated to {new_weight}"
        

    def update_macros(self, food, weight, sign=1):
        self.sum_of_proteins += food.get_proteins(weight*sign)
        self.sum_of_fats +=     food.get_fats(weight*sign)
        self.sum_of_carbs +=    food.get_carbs(weight*sign)
        self.sum_of_calories += food.get_calories(weight*sign)


    def get_foods(self):
        return list(self.foods.keys())


    def __repr__(self) -> str:
        return f"{self.foods}"


    def __str__(self) -> str:
        return f"Sum of proteins: {self.sum_of_proteins}g\nSum of fats: {self.sum_of_fats}g\nSum of carbs: {self.sum_of_carbs}g\nSum of calories: {self.sum_of_calories}kcal"
    
