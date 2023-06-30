from pymongo import MongoClient
import os

# Read env vars like this : os.environ.get('KEY_THAT_MIGHT_EXIST', default_value)

class MongoDBSingleton:
    _instance = None
    
    @staticmethod
    def get_instance():
        if MongoDBSingleton._instance is None:
            MongoDBSingleton()
        return MongoDBSingleton._instance
    
    def __init__(self):
        if MongoDBSingleton._instance is not None:
            raise Exception("MongoDBSingleton should be accessed through get_instance() method.")
        else:
            MongoDBSingleton._instance = self
            self.client = MongoClient('mongodb://localhost:27017/')
    
    