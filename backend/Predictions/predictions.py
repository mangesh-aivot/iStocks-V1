from  Scrappers.scrappers import economictimes,moneycontrol,investing,livemint,businesstoday,cnbc,zeebiz
from Datamanagement.datamanagement import save_news ,save_predictions, combine_results ,  filter_old_ticker , precomputed ,combine_dfs , fetch_results
from Filtering.filtering import company_finding 
from Sentimentanalysis.sentimentanalysis import sentiment_analysis , sentiment_formatter 
from Predictions_util.predictions_util import predictions ,technical_indct ,  cmp_volume ,format_value

import yfinance as yf
from datetime import date, timedelta , datetime
import time
import pandas as pd
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from aiojobs import create_scheduler



app = FastAPI()
origins = [
    "http://localhost:5174",  # Add your frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/gettechnicals")
def gettechnicals():
    current_dir = os.path.dirname(__file__)
    directory = os.path.join(current_dir, 'Data', 'Results')


    today = datetime.now()

    three_days_ago = today - timedelta(days=3)


    dataframes = []

    for filename in os.listdir(directory):

        if filename.startswith("Predictions_on_") and filename.endswith(".csv"):

            date_str = filename.split("_on_")[1].split("_at_")[0]
            time_str = filename.split("_at_")[1].replace('.csv', '')
            

            file_datetime_str = f"{date_str} {time_str}"
            file_datetime = datetime.strptime(file_datetime_str, '%Y-%m-%d %I-%M%p')
            

            if three_days_ago <= file_datetime <= today:

                df = pd.read_csv(os.path.join(directory, filename))

                df['Date'] = file_datetime_str

                dataframes.append(df)


    df = pd.concat(dataframes)
    df.reset_index(inplace=True)
    df = technical_indct(df)
    df = df.to_dict(orient='records')

    return  df

@app.get("/getsentiment")
def getsentimentanalysis():
    current_dir = os.path.dirname(__file__)
    directory = os.path.join(current_dir, 'Data', 'Results')

    today = datetime.now()

    three_days_ago = today - timedelta(days=3)


    dataframes = []

    for filename in os.listdir(directory):

        if filename.startswith("Predictions_on_") and filename.endswith(".csv"):

            date_str = filename.split("_on_")[1].split("_at_")[0]
            time_str = filename.split("_at_")[1].replace('.csv', '')
            
            file_datetime_str = f"{date_str} {time_str}"
            file_datetime = datetime.strptime(file_datetime_str, '%Y-%m-%d %I-%M%p')
            
            if three_days_ago <= file_datetime <= today:
                df = pd.read_csv(os.path.join(directory, filename))
                df['Date'] = file_datetime_str
                dataframes.append(df)


    df = pd.concat(dataframes)
    df = df[['Company Name','Sentiment','Date']]
    df = sentiment_formatter(df)
    print(df)
    df.reset_index(inplace=True)
    df = df.to_dict(orient='records')


    return  df



@app.get("/getnews")
def getnews():
    current_dir = os.path.dirname(__file__)
    directory  = os.path.join(current_dir,'Data','News')



    today_date = datetime.now().strftime('%Y-%m-%d')

    files = os.listdir(directory)

    today_files = [f for f in files if today_date in f]


    if len(today_files) == 1:
        file_path = os.path.join(directory, today_files[0])
        

        df = pd.read_csv(file_path)

        df.dropna(inplace=True)
        summaries = df['Summary']

        summaries_list = summaries.tolist()

    return {"News":summaries_list}



@app.get("/indices/{index_name}")
def indicies(index_name: str):
    tickers_list = {
    'Nifty': '^NSEI',
    'Sensex': '^BSESN',
    'Bank Nifty': '^NSEBANK'
    }
    ticker = tickers_list.get(index_name)
    if ticker :
        stock = yf.Ticker(ticker)
        td = date.today()
        yd = td - timedelta(days=3)
       
        live_data = stock.history(start=yd, end=td+ pd.DateOffset(days=1), interval='1d')
        previous_close = live_data['Close'].iloc[-2]
        current_price = live_data.iloc[-1]['Close']
        change = current_price - previous_close
        change_percentage = ((current_price - previous_close) / previous_close) * 100
        change_percentage = round(change_percentage, 2)
        formatted_price = f"{current_price:,.2f}"
        formatted_change = f"{change:+,.2f}"  # The '+' sign ensures the sign is always shown
        formatted_change_percentage = f"({abs(change_percentage):.2f}%)"
 
   
    return  {"name": index_name, "price": formatted_price , "change":f"{formatted_change} {formatted_change_percentage}"}



@app.get("/get-predictions")
async def get_prediction():


    ## df = combine_dfs(economictimes(),moneycontrol(),investing(),livemint(),businesstoday(),cnbc(),zeebiz())
    # df = combine_dfs(economictimes(),moneycontrol(),investing(),livemint(),businesstoday(),cnbc())
    # save_news(df) 

    # df = company_finding(df)

    # print(f"Collected from News {df}")


    # df = df[df["Mentions"] >= 3 ]

    # print(f"Before Filtering{df}")
    # print("###########")

    # df = filter_old_ticker(df) #filters repetaions if repeated agian before 3 weeks 
    # print(f"After Filtering {df}")

    
    # if not df.empty:
    #     df = sentiment_analysis(df)
    #     # df = sentiment_analysis_LLAMA(df)

    # print(df)

    # if not df.empty:    
    #     df = predictions(df)
    # if df.empty:
    #     print("No Prediction from predictions function")
    # print(df)
    # df = precomputed(df)
    # df = filter_old_ticker(df)

    # if not df.empty:
    #     save_predictions(df)
    # # df = pd.read_csv('/home/rahul-/Projects/UI/StockApp/backend/Data/Results/Predictions_on_2024-06-26_at_12-59PM.csv')
    ## print(df)
    df = fetch_results()
    if df.empty:
        return {"Message":"No prediction for Today"}
    

    ## df = pd.read_csv(r'C:\Users\ASUS\Projects\UI\StockApp\backend\Data\Results\Predictions_on_2024-07-09_at_10-50AM.csv')
    df = cmp_volume(df)
    df = technical_indct(df)
    df = sentiment_formatter(df)

    df = df.fillna('')
    ## df = pd.read_csv(r"C:\Users\ASUS\Projects\UI\Stock-app\backend\Predictions\Data\Results\Predictions_on_2024-07-17_at_11-54AM.csv")
    predictions_dict = df.to_dict(orient='records')

    ## predictions_dict = [{'Unnamed: 0': 0, 'Company Name': 'Trent', 'Company Symbol': 'TRENT', 'TP1': 5038, 'TP2': 5106, 'TP3': 5165,'SL':4966,'Time':'0-3 Weeks','CMP':4990,'Volume':33546,'Technical':'Strong Buy','Sentiment':'Strong','News':"This is sample for testing the news box . Adding random words to make it long ajndfkjdsnfkjndskjfnkjsdd  ds fdskfjsdkjfkjsdfkjskjdnfkjsdkjf "}]
    return  predictions_dict


