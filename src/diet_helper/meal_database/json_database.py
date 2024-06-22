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
                with open(json_file_path, 'w') as f:
                    return json_file_path
            else: 
                return exit('Please create json file')   

    def get_meals(self):
        return self.load()

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