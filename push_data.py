import os 
import sys
import json
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo 
from frauddetection.exception.exception import FraudDetectionException
from frauddetection.logging.logger import logging

class FraudDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise FraudDetectionException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise FraudDetectionException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[database]
            
            self.collection = self.database[collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise FraudDetectionException(e, sys)
if __name__=="__main__":
    FILE_PATH = "Fraud_data/creditcard.csv"
    DATABASE = "RAHULAI"
    Collection = "FraudData"
    Fraudobj = FraudDataExtract()
    records = Fraudobj.csv_to_json_convertor(file_path=FILE_PATH)
    no_of_records = Fraudobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)