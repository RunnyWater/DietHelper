import os
import json 


class JsonMealManager:
    def __init__(self, json_file_path='json/meals.json'):
        self.json_path = self.get_database(json_file_path)
        self.data = self.load()

    def get_database(self, json_file_path='json/meals.json'):
        if os.path.exists(json_file_path):
            return json_file_path
        else:
            if input(f"{json_file_path} not found, do you want to create it? (y/n)") == 'y': 
                os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
                return json_file_path
            else: 
                return exit('Please create json file')   

    def get_meals(self)-> dict:
        return self.load()

    def get_meal_by_id(self, id)->dict:
        if id in self.data.keys():
            return self.data[id]
        else:
            print(f"Database does not have a meal with id of {id}")
            return {}

    def change_food_weight(self, id:int,  food_name:str, new_weight:int):
        self.data[id][food_name] = new_weight
        self.save()

    def add_food(self, id:int, new_food:dict):
        self.data[id].update(new_food)
        self.save()
        
    def insert_meal(self, foods:dict):
        id = len(self.data)
        self.data[id] = foods

    def update_food_name(self, id:int, old_name:str, new_name:str):
        self.data[id][new_name] = self.data[id].pop(old_name)
        self.save()

    def delete_meal(self, id:int):
        self.data.pop(id)
        self.save()

    def delete_food(self, id:int, food_name:str):
        self.data[id].pop(food_name)
        self.save()

    def load(self):
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def save(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.data, f, indent=4)