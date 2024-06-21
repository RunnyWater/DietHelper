from diet_helper import MacroManager, FoodLister, Foods, Meal

from dotenv import load_dotenv
import os


def main_function():
    test = Foods(db_type='json')
    print(test)    

    
if __name__ == "__main__":
    main_function()