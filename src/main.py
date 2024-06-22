from diet_helper import MacroManager, FoodLister, Foods, Meal, copy



def main_function():
    # test = Foods(db_type='mongo')
    # copy.copy_foods_to_local_json(test.foods, 'json/local_copy.json')
    test = Meal(0, foods={'egg': 1, 'chicken breast': 0.5}, db_type='mongo')
    # test.add_food('chicken breast', 0.5)
    print(test)

if __name__ == "__main__":
    main_function()
