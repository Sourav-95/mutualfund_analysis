import glob
import os
import sys
from src.exception import CustomException
from src.logger import logging

def fetch_csv_files(folder_path):
    try:
        # Fetch all CSV files in the given folder
        print("Ingesting all the Files......................................")
        print("=============================================================\n")
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
        if not csv_files:
            print("------------No CSV files found in the specified folder------------------")
        else:
            logging.info(f"Fetched {len(csv_files)} CSV files from {folder_path}")
            for file in csv_files:
                print(f"{file}")
            print("\nAll files Ingested............................................")

        return csv_files

    except Exception as e:
        raise CustomException(e, sys)