import os
import json 

class JsonFoodManager:
    def __init__(self, json_file_path='json/foods.json'):
        self.json_path = self.get_database(json_file_path)
        self.data = self.load()


    def get_database(self, json_file_path='json/foods.json'):
        if os.path.exists(json_file_path):
            return json_file_path
        else:
            if input(f"{json_file_path} not found, do you want to create it? (y/n)") == 'y': 
                os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
                with open(json_file_path, 'w') as f:
                    return json_file_path


    def get_foods(self):
        return self.load()


    def get_food(self, name):
        name = name.lower()
        if name in self.data:
            return self.data[name]
        else:
            return "There is no such food in database"
 
    def get_variants(self, name, stringify=False):
        variants = self.get_food(name)['variants']
        if stringify:
            return f'"{name}" variants:\n'+'\n'.join([f"{key} - {value}g" for key, value in variants.items()])
        else:
            return variants

    def insert_food(self, name, p, f, c):
        name = name.lower()
        self.data[name] = {'name': name, 'p': p, 'f': f, 'c': c, 'variants': None}
        self.save()


    def delete_food(self, name):
        name = name.lower()
        if name in self.data:
            del self.data[name]
            self.save()
            return f"{name} was deleted"
        else:
            return "There is no such food in database"

    def delete_variant(self, food_name, variant_name=None):
        if variant_name is None:
            printed_version = ''
            variants = self.get_food(food_name)['variants']
            for variant in variants.keys():
                printed_version += f"{variant} with weight {variants[variant]} \n"
            return 'Please input the name of the variant you want to delete'+'\n'+printed_version

        food_name = food_name.lower()
        variant_name = variant_name.lower()
        if food_name in self.data:
            if variant_name in self.data[food_name]['variants']:
                del self.data[food_name]['variants'][variant_name]
                self.save()
                return f"{variant_name} was deleted from {food_name}"
            else:
                return "There is no such variant in database"
        else:
            return "There is no such food in database"

    def add_variant(self, food_name=str, new_variant=dict) -> str:
        if not self.variant_correctness_check(new_variant):
            return "Variant is not correct, please check it again"
        food_name = food_name.lower()

        try: 
            new_variant = {key.lower(): int(value) for key, value in new_variant.items()}
            variants = self.data[food_name]['variants']
        except Exception as e:
            return "There was an error while searching food: " + str(e)
        
        if variants is None:
            variants = {}
        else:
            name_exists = False
            weight_exist = False
            names = []
            weights = []
            for name in new_variant.copy().keys():
                if name in variants.keys():
                    name_exists = True
                    names.append(name)
                    del new_variant[name]
                if new_variant.get(name) in variants.values():
                    weight_exist = True
                    weights.append(new_variant.get(name))
                    del new_variant[name]

            if name_exists:
                print( f"{', '.join(names)} already exist in dataset and will not be added/updated")
            if weight_exist:
                print( f"{', '.join(weights)} already exist in dataset and will not be added/updated")
            del name_exists, weight_exist, names, weights, name

        variants.update(new_variant)
        try:
            if len(new_variant) > 0:
                self.data[food_name]['variants'] = variants
                self.save()
                return f"{', '.join(new_variant.keys())} added to {food_name}" 
            else:
                return f"Unfortunately no new variant added to {food_name}"
        except Exception as e:
            return "There was an error while adding new variant to food: " + str(e)


    def update_variant(self, name=str, variant_name=None, new_weight=None) -> str:
        if variant_name is None or new_weight is None:
            variants = self.get_food(name)['variants']
            printed_version = ''
            for variant in variants.keys():
                printed_version += f"\n{variant} with weight {variants[variant]}"
            return 'Please input the name of the variant you want to update'+printed_version
        elif not self.check_type(new_weight): raise 'The value must be an integer'
        else:
            try:
                name = name.lower()
                variant_name = variant_name.lower()
                self.data[name]['variants'][variant_name] = new_weight
                self.save()
                return f"{name}:{variant_name} updated to {new_weight}"
            except Exception as e:
                return "There was an error while updating variant: " + str(e)

    def update_food(self, name=str, p=None, f=None, c=None) -> str:
        if p is None and f is None and c is None:
            return "You need to provide at least one parameter to update"
        try:
            name = name.lower()
            if p is not None:
                self.update_proteins(name,p)
            if f is not None:
                self.update_fats(name,f)
            if c is not None:
                self.update_carbs(name,c)
            return f"{name} updated"
        except Exception as e:
            return "There was an error while updating food: " + str(e)


    def update_proteins(self, name=str, p=int) -> str:
        if not self.check_type(p): raise 'The value must be an integer'
        try:
            self.data[name]['p'] = p
            return f"{name} updated, now it has {p} proteins"
        except Exception as e:
            return "There was an error while updating protein: " + str(e)
    

    def update_fats(self, name=str, f=int) -> str:
        if not self.check_type(f): raise 'The value must be an integer'
        try:
            self.data[name]['f'] = f
            return f"{name} updated, now it has {f} fats"
        except Exception as e:
            return "There was an error while updating fats: " + str(e)
    

    def update_carbs(self, name=str, c=int) -> str:
        if not self.check_type(c): raise 'The value must be an integer'
        try:
            self.data[name]['c'] = c
            return f"{name} updated, now it has {c} carbs"
        except Exception as e:
            return "There was an error while updating carbs: " + str(e)

    def check_type(self, value=None) -> bool:
        if type(value) == int:
            return True
        else:
            return False

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


    def variant_correctness_check (self, variants=dict) -> bool:
        if type(variants) == dict:
            for weight in variants.values():
                try :
                    int(weight)
                except:
                    return False
            return True
        else:
            return False