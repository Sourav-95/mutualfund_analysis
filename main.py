# main.py

from src.components.data_ingestion import fetch_csv_files
from src.components.data_transformation import process_files, merge_dataframes
from src.components.gsheet_export import export_to_gsheet
from src.logger import logging
from src.exception import CustomException
import sys

if __name__ == "__main__":
    try:
        logging.info("Starting the script")

        # Folder path and credentials
        folder_path = r'G:\Fund_analysis\Raw_data'
        credentials_path = r'G:\Fund_analysis_cred\cred_file.json'
        spreadsheet_id = '15Tx7fwzYAQLlXEz8nr3zcSuIWT1gn0GnhjmzCnpW5PE'

        # Ingest files
        logging.info("Fetching CSV files")
        csv_files = fetch_csv_files(folder_path)

        # Process the files by identifier
        logging.info("Processing files")
        files_with_one = [file for file in csv_files if '1' in file]
        files_with_two = [file for file in csv_files if '2' in file]
        files_with_three = [file for file in csv_files if '3' in file]

        df_1 = process_files(files_with_one, '1')
        df_2 = process_files(files_with_two, '2')
        df_3 = process_files(files_with_three, '3')

        # Merge and transform DataFrames
        logging.info("Merging DataFrames")
        combined_df = merge_dataframes(df_1, df_2, df_3)

        # Export the combined data to Google Sheets
        if combined_df is not None:
            logging.info("Exporting to Google Sheets")
            export_to_gsheet(combined_df, credentials_path, spreadsheet_id)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise CustomException(e, sys)
