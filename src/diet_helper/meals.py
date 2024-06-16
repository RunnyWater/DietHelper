import meal 

class Meals:
    def __init__(self, foods):
        self.meals = []
        for food in foods.getNames():
            self.meals.append(meal.Meal(food))
    
# TODO: finish meals functionality