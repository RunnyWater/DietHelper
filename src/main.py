from diet_helper import MongoManager, MacroManager, FoodLister

from dotenv import load_dotenv
import os


def main_function():
    load_dotenv()
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')

    db_manager = MongoManager(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)
    macro_manager =MacroManager(db_manager.food_collection)
    diet_helper = FoodLister(db_manager.food_collection)
    # print(macro_manager.get_info_with_variant('egg', get_calories=True, get_protein=True))
    print(diet_helper.list_best_protein_per_calorie_foods())

    db_manager.close()


if __name__ == "__main__":
    main_function()