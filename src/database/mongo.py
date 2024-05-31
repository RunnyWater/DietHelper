import pymongo

class MongoManager:
    def __init__(self, con_string, database_name, food_collection_name):
        self.client = self.connect_to_database(con_string)
        self.db = self.client[f'{database_name}']
        self.food_collection = self.db[f'{food_collection_name}']

    def connect_to_database(self, con_string):
        client = pymongo.MongoClient(con_string)
        print("Connected to MongoDB")
        return client


    def insert_food(self, name=str, p=str, f=str, c=str) -> str:
        try: 
            self.food_collection.insert_one({"_id": self.food_collection.count_documents(), "name":name.lower(), "p":p, "f":f, "c":c, "variants":None})
            return f"{name} added to database with p: {p}, f: {f}, c: {c}"
        except Exception as e:
            return "There was an error while adding new food: " + str(e)
    

    def variant_correctness_check (self, variants=dict) -> bool:
        for weight in variants.values():
            try :
                int(weight)
            except:
                return False
        return True

    def add_variant(self, food_name=str, new_variant=dict) -> str:
        if not self.variant_correctness_check(new_variant):
            return "Variant is not correct, please check it again"
        food_name = food_name.lower()
        try: 
            new_variant = {key.lower(): str(value) for key, value in new_variant.items()}
            variants = self.food_collection.find_one({"name":food_name})['variants']
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
                self.food_collection.update_one({"name":food_name}, {"$set":{"variants":variants}})
                return f"{', '.join(new_variant.keys())} added to {food_name}" 
            else :
                return f"Unfortunately no new variant added to {food_name}"
        except Exception as e:
            return "There was an error while adding new variant to food: " + str(e)
    

    def update_variant(self, food_name=str, variant_name=str, new_value=str or int) -> str:
        new_value = str(new_value)
        variant_name = variant_name.lower()
        try:
            variants = self.food_collection.find_one({"name":food_name.lower()})['variants']        
        except Exception as e:
            return "There was an error while searching food: " + str(e)
        if variants is None or variant_name not in variants.keys():
            return "There is no such food variant in database"
        else:
            try :
                variants[variant_name] = new_value
                self.food_collection.update_one({"name":food_name}, {"$set":{"variants":variants}})
                return f"{food_name}, {variant_name} updated to {new_value}"
            except Exception as e:
                return "There was an error while updating variant: " + str(e)   


    def delete_variant(self, food_name=str, variant_name=None ) -> str:
        food_name = food_name.lower()
        try:
            variants = self.food_collection.find_one({"name":food_name.lower()})['variants']        
        except Exception as e:
            return "There was an error while searching food: " + str(e)
        if variant_name is None:
            printed_version = ''
            for variant in variants.keys():
                printed_version += f"{variant} with weight {variants[variant]} \n"
            while True:
                print("Please type the name of the variant you want to delete")
                variant_name = input(printed_version)
                variant_name=variant_name.strip().lower()
                if variant_name not in variants.keys() and variant_name != 'exit':
                    print("There is no such food variant in database, please type again, or type 'exit' to exit")
                    print(variant_name, " WAHJTAAVAFAk")
                else:
                    break
        if variant_name != 'exit':
            try:
                del variants[variant_name.strip().lower()]
                self.food_collection.update_one({"name":food_name}, {"$set":{"variants":variants}})
                return f"From '{food_name}'-food '{variant_name}'-variant was deleted"
            except  Exception as e:
                return "There was an error while deleting variant: " + str(e)
        else:
            return "Exited with 'exit' command"

            
        

    def close(self) -> None:
        if self.client:
            print("Closing connection to MongoDB")
            self.client.close()
        else:
            print("No connection to close")
