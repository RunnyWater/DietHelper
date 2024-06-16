from diet_helper import MacroManager, FoodLister, Foods, Meal

from dotenv import load_dotenv
import os


def main_function():
    load_dotenv()
    # Change to your connection string and database name
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    # Change to your database type
    db_type = 'mongo'

    # foods = Foods(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME, db_type)

    
if __name__ == "__main__":
    main_function()