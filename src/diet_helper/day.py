from meal import Meal
from datetime import date

class Day:
    def __init__(self):
        self.meals = {}
        self.date = ''
        self.sum_of_proteins = 0
        self.sum_of_fats = 0
        self.sum_of_carbs = 0
        self.sum_of_calories = 0
        self.note = ''


# TODO: finish day functionality