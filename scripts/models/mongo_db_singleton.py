from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
# Read env vars like this : os.environ.get('KEY_THAT_MIGHT_EXIST', default_value)


class MongoDBSingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if MongoDBSingleton.__instance is None:
            MongoDBSingleton()
        return MongoDBSingleton.__instance

    def __init__(self):
        if MongoDBSingleton.__instance is not None:
            raise Exception("Ce Singleton est déjà instancié ! Utilisez la méthode get_instance().")
        else:
            MongoDBSingleton.__instance = self
            self.client = MongoClient(os.environ.get('MONGO_HOST', 'localhost'), int(os.environ.get('MONGO_PORT', 27017)))
            self.db = self.client[os.environ.get('MONGO_DB_NAME')]

    def get_collection(self, collection_name):
        return self.db[collection_name]