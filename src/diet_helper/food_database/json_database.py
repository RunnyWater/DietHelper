import os
import json 

class JsonManager:
    def __init__(self, json_file_path='json/foods.json'):
        self.json_path = self.get_database(json_file_path)
        
        self.data = None

    def get_database(self, json_file_path='json/foods.json'):
        if os.path.exists(json_file_path):
            return json_file_path
        else:
            if input(f"{json_file_path} not found, do you want to create it? (y/n)") == 'y': 
                os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
                with open(json_file_path, 'w') as f:
                    return json_file_path
                

    def load(self):
        with open(self.json_file_path, 'r') as f:
            self.data = json.load(f)

    def save(self):
        with open(self.json_file_path, 'w') as f:
            json.dump(self.data, f)


test_json = JsonManager()
