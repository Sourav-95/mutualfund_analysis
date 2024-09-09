import pandas as pd
import glob
import os

folder_path = 'mutualfund_analysis/Raw_data'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

combined_df.to_csv('mutualfund_analysis/Raw_data/combine.csv', index=False)