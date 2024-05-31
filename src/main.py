from database import MongoManager
from dotenv import load_dotenv
import os


def main_function():
    load_dotenv()


    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    db_manager = MongoManager(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)
    print(db_manager.add_variant('egg', {'Xl': '60'}))
    
    db_manager.close()


if __name__ == "__main__":
    main_function()