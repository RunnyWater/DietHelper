from diet_helper import MacroManager, FoodLister, Foods, Meals, copy



def main_function():
    test = Meals(db_type='mongo')
    print(test.insert_meal({'egg': 1.2, 'chicken breast': 3}))
    print(test)
if __name__ == "__main__":
    main_function()
