from diet_helper import MacroManager, FoodLister, Foods

from dotenv import load_dotenv
import os


def main_function():
    load_dotenv()
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    db_type = 'mongo'

    foods = Foods(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME, db_type)
    diet_helper = FoodLister(foods)
    macro = MacroManager(foods)


if __name__ == "__main__":
    main_function()