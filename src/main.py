from diet_helper import MacroManager, FoodLister, Foods, Meals, copy



def main_function():
    test = Meals(db_type='mongo')
    print(test.get_meal_by_id(0).get_macros())

if __name__ == "__main__":
    main_function()

