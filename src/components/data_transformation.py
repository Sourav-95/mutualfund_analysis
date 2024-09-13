import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
import sys


def process_files(files, identifier):
    logging.info(f"Processing files for identifier: {identifier}")
    dataframes_list = []
    
    for file in files:
        logging.info(f"Reading file: {file}")
        df = pd.read_csv(file)

        # Fund type identification logic
        if 'Debt' in file:
            df['Fund Type'] = 'Debt'
        elif 'Equity' in file:
            df['Fund Type'] = 'Equity'
        elif 'Hybrid' in file:
            df['Fund Type'] = 'Hybrid'
        elif 'Commodity' in file:
            df['Fund Type'] = 'Commodity'

        logging.info(f"Processed file: {file}")
        dataframes_list.append(df)

    if dataframes_list:
        combined_df = pd.concat(dataframes_list, ignore_index=True)
        logging.info(f"Combined DataFrame {identifier}: Length = {len(combined_df)}")
        return combined_df
    else:
        logging.warning(f"No files with '{identifier}' in the name were found.")
        return None

def merge_dataframes(df_1, df_2, df_3):
    logging.info("Merging DataFrames")
    if df_1 is not None and df_2 is not None and df_3 is not None:
        combined_df = pd.merge(df_1, df_2, on=df_1.columns[0], how='outer')
        combined_df = pd.merge(combined_df, df_3, on=combined_df.columns[0], how='outer')

        # Drop columns and apply transformations
        columns_to_drop = [col for col in combined_df.columns if col.endswith('_x') or col.endswith('_y')]
        combined_df.drop(columns=columns_to_drop, inplace=True)

        columns_to_keep = [col for col in combined_df.columns if 'Other' not in col]
        combined_df = combined_df[columns_to_keep]

        combined_df.replace(0, np.nan, inplace=True)
        float_cols = combined_df.select_dtypes(include='float64').columns
        for col in float_cols:
            if col != 'Expense Ratio':
                combined_df[col] = combined_df[col].round(3)

        logging.info("DataFrames merged and cleaned")
        return combined_df
    else:
        logging.warning("One or more DataFrames were None, skipping merge.")
        return None
