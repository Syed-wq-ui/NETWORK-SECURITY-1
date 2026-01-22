import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Get SSL certificate path for MongoDB Atlas connection
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        pass

    def csv_to_json_convertor(self, file_path):
        try:
            # Read CSV file
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            
            # FIXED: Correct way to convert DataFrame to a list of JSON records
            # Your previous version used .values() on a string, which caused the error
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database_name = database
            self.collection_name = collection
            self.records = records

            # Added tlsCAFile=ca to handle SSL connection issues common in local environments
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.db = self.mongo_client[self.database_name]
            self.col = self.db[self.collection_name]
            
            self.col.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    # Using 'r' prefix for the Windows path to avoid Unicode escape errors
    FILE_PATH = r"C:\SECURITY\Network Security\Network_Data\phisingData.csv"
    DATABASE = "FarooqTech"
    Collection = "NetworkData"
    
    networkobj = NetworkDataExtract()
    
    # 1. Convert CSV to JSON records
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(f"Total records converted: {len(records)}")
    
    # 2. Insert into MongoDB
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(f"Successfully inserted {no_of_records} records into MongoDB.")