import os
import pandas as pd
from datetime import datetime

def process_csv_files(folder_path):
    # Get today's date in the required format
    today_str = datetime.now().strftime('%Y-%m-%d')

    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Dictionary to hold dataframes for each date
    date_file_map = {}

    for file in csv_files:
        try:
            # Extract date from the filename
            file_date = file.split('_')[2]
            
            # Skip today's files
            if file_date == today_str:
                continue
            print(file_date)
            # Load the CSV file into a dataframe
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            # Add the dataframe to the map, merging if the date already exists
            if file_date in date_file_map:
                date_file_map[file_date] = pd.concat([date_file_map[file_date], df]).drop_duplicates()
            else:
                date_file_map[file_date] = df

            # Removing the original file
            os.remove(file_path)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    # Ensure the output directory exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Saving merged dataframes to new files
    for file_date, df in date_file_map.items():
        try:
            new_filename = f"News_on_{file_date}_total.csv"
            new_file_path = os.path.join(folder_path, new_filename)
            df.to_csv(new_file_path, index=False)
        except Exception as e:
            print(f"Error saving file for date {file_date}: {e}")


process_csv_files(r'C:\Users\ASUS\Projects\UI\Stock-app\backend\Predictions\Data\News')
