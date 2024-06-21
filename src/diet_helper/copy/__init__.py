import json
import os

def copy_foods_to_local_json(foods=dict, json_file_path='json/foods.json'):
    if not os.path.exists(json_file_path):
        if input(f"{json_file_path} not found, do you want to create it? (y/n)") == 'y': 
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        else: 
            return exit('Please create json file')
    data = {}
    for food_name in foods.keys():
        data[food_name] = foods[food_name].get_info_for_json()
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)