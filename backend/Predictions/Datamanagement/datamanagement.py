import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz
import ntplib
from pytz import timezone
import os
from pandas.errors import EmptyDataError




def save_news(df):
    try:
        # Fetch current time from NTP server
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        utc_now = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
    except Exception as e:
        print(f"Error fetching NTP time: {e}. Falling back to local machine time.")
        # Fallback to local machine time using pytz
        utc_now = datetime.now(pytz.utc)


    ist_offset = timedelta(hours=5, minutes=30)
    ist_now = utc_now + ist_offset

    current_date_ist = ist_now.strftime('%Y-%m-%d')

    file_name = f"News_on_{current_date_ist}_"  
    # saving the news 

    cur_dir = os.path.dirname(__file__)

    path = os.path.join(cur_dir, '..', 'Data', 'News', f'{file_name}.csv')

    df.to_csv(path)






def save_predictions(results_df):
    utc_now = datetime.now(pytz.utc)

    # Convert to IST
    ist = timezone('Asia/Kolkata')
    ist_now = utc_now.astimezone(ist)
    current_date_ist = ist_now.strftime('%Y-%m-%d')
    current_time_ist = ist_now.strftime('%I-%M%p')

    # Define folder path
    # folder_path = "C:\\Users\\ASUS\\Projects\\UI\\StockApp\\backend\\Predictions\\Data\\Results"

    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir,'..','Data','Results')
    folder_path = path


    
    # Check if any file for today exists
    files = os.listdir(folder_path)
    today_files = [f for f in files if f.startswith(f"Predictions_on_{current_date_ist}") and f.endswith(".csv")]

    if today_files:  #if file already exists
        # Load existing data
        file_path = os.path.join(folder_path, today_files[0])
        existing_df = pd.read_csv(file_path)
        if 'Unnamed: 0' in existing_df.columns:
            existing_df.drop(columns=['Unnamed: 0'], inplace=True)
            
        # Append new data
        combined_df = pd.concat([existing_df, results_df], ignore_index=True)
        
        combined_df.drop_duplicates(subset=['Company Symbol'], inplace=True)
        
        # Save combined data
        combined_df.to_csv(file_path, index=False)
        print(f"Updated existing file: {file_path}")
    else:
        # Create a new file name
        file_name_r = f"Predictions_on_{current_date_ist}_at_{current_time_ist}.csv"
        new_file_path = os.path.join(folder_path, file_name_r)
        
        results_df.to_csv(new_file_path, index=False)
        print(f"Created new file: {new_file_path}")

def combine_results():

    # folder_path = 'C:/Users/ASUS/Projects/UI/StockApp/backend/Predictions/Data/Results'
    current_dir = os.path.dirname(__file__)
    folder_path = os.path.join(current_dir,'..','Data','Results')

    today =  datetime.today().date()

    all_dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # Extract the date from the filename
            date_str = filename.split('_')[2]  #the date is in the third part of the split filename

            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert to date object
            
            if date == today :
                continue 

            csv_file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(csv_file_path)

            df['Date'] = date

            all_dfs.append(df)

    combined_df = pd.concat(all_dfs, ignore_index=True)


    combined_df = combined_df.sort_values(by=['Company Symbol', 'Date'])

    # final_df = combined_df.drop_duplicates(subset=['Company Symbol'], keep='first')

    combined_df = combined_df.sort_values(by='Date')


    return combined_df



def filter_old_ticker(df2):
    # Check if df2 is empty
    if df2.empty:
        return df2

    df1 = combine_results()
    # Ensure the 'Date' column in df1 is in datetime format
    df1['Date'] = pd.to_datetime(df1['Date'])
    
    today = datetime.now()
    
    # Calculate the threshold date (3 weeks ago)
    threshold_date = today - timedelta(weeks=3)
    
    def should_keep_ticker(ticker):
        # Check if the ticker is in df1
        if ticker in df1['Company Symbol'].values:
            dates = df1[df1['Company Symbol'] == ticker]['Date']
            # Check if any of the dates are within the last 3 weeks
            if any(dates > threshold_date):
                return False
        return True
    
    # Apply the function to filter df2
    df2_filtered = df2[df2['Company Symbol'].apply(should_keep_ticker)]
    
    return df2_filtered


def precomputed(df):
    # folder_path = "C:\\Users\\ASUS\\Projects\\UI\\StockApp\\backend\\Predictions\\Data\\Results"
    current_dir = os.path.dirname(__file__)
    folder_path = os.path.join(current_dir,'..','Data','Results')

    today_date = datetime.now().strftime('%Y-%m-%d')

    files = os.listdir(folder_path)

    today_files = [f for f in files if f.startswith(f"Predictions_on_{today_date}") and f.endswith(".csv")]

    if not today_files: #if precomputed data not available
        return df
    else:  #if precomputed data available

        # Load precomputed data
        for file in today_files:
            file_path = os.path.join(folder_path, file)

            try:
                temp_df = pd.read_csv(file_path) #if the file exists without columnns 
            except EmptyDataError:
                continue

            if temp_df.empty:
                continue
            if df.empty:
                df = temp_df
            else:
                df = pd.concat([df, temp_df], ignore_index=True)

        if 'Unnamed: 0' in df.columns:
            df.drop(columns=['Unnamed: 0'], inplace=True)
            
        df.drop_duplicates(subset=['Company Symbol'], inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df

def combine_dfs(*dfs):
    df = pd.concat(dfs,axis=0)
    df.drop_duplicates(inplace=True)
    df = df.reset_index(drop=True)
    return df

def fetch_results():
    current_dir = os.path.dirname(__file__)
    folder_path = os.path.join(current_dir,'..','Data','Results')

    # Get today's date in the format used in file names
    today_date = datetime.now().strftime('%Y-%m-%d')
    file_name_pattern = f'Predictions_on_{today_date}_at_'

    # List all files in the directory
    files = os.listdir(folder_path)

    # Check if there's a file with today's date
    file_to_load = None
    for file in files:
        if file.startswith(file_name_pattern) and file.endswith('.csv'):
            file_to_load = file
            break

    # Load the file if it exists
    if file_to_load:
        file_path = os.path.join(folder_path, file_to_load)
        df = pd.read_csv(file_path)
        
    else:
        df = pd.DataFrame()

    return df
    