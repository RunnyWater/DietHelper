import pymongo 
import datetime
from dotenv import load_dotenv
import os

class MongoDayManager:
    def __init__(self, con_string=None, database_name=None, day_collection_name='day'):
        if con_string is None or database_name is None:
            load_dotenv()
            
            self.con_string = os.getenv('CONNECTION_STRING')
            self.database_name = os.getenv('DATABASE_NAME')
        else:
            self.con_string = con_string
            self.database_name = database_name
        self.day_collection_name = day_collection_name
        self.connected = False
        self.client = None


    def connect_to_database(self):
        try:
            client = pymongo.MongoClient(self.con_string)
            self.connected = True
            return client
        except Exception as e:
            return "There was an error while connecting to database: " + str(e)

    def get_collection(self):
        self.client = self.connect_to_database()
        try:
            db = self.client[f'{self.database_name}']
            return db[f'{self.day_collection_name}']
        except Exception as e:
            self.close_connection()
            return "There was an error while getting collection: " + str(e)


    def close_connection(self) -> None:
        try:
            self.client.close()
            self.connected = False
            print("Connection was successfully closed")
        except Exception as e:
            print("There was an error while closing connection: " + str(e))


    def get_days(self):
        day_collection = self.get_collection()
        try: 
            days = day_collection.find()
            return days
        except Exception as e:
            self.close_connection()
            return "There was an error while getting days: " + str(e)


    def get_day(self, date:str):
        if not self.is_date_in_format(date):
            print("Wrong date format")
            return None
        day_collection = self.get_collection()
        try: 
            day = day_collection.find_one({"name":da.lower()})
            return day
        except Exception as e:
            self.close_connection()
            return "There was an error while getting food: " + str(e)


    def is_date_in_format(self, date:str):
        try :
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False