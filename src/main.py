from diet_helper import MacroManager, FoodLister, Foods, Meal, copy



def main_function():
    test = Foods(db_type='mongo')
    print(test)
    # test.add_food('chicken breast', 31, 4, 0)
    copy.copy_foods_to_local_json(test.foods, 'json/local_copy.json')
    
if __name__ == "__main__":
    main_function()