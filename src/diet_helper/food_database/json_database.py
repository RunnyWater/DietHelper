# TODO: add json support


import json 

class JsonManager:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = None

    def load(self):
        with open(self.json_file_path, 'r') as f:
            self.data = json.load(f)

    def save(self):
        with open(self.json_file_path, 'w') as f:
            json.dump(self.data, f)