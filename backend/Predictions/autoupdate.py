from  Scrappers.scrappers import economictimes,moneycontrol,investing,livemint,businesstoday,cnbc,zeebiz,scrape_news
from Datamanagement.datamanagement import save_news ,save_predictions, combine_results ,  filter_old_ticker , precomputed ,combine_dfs , fetch_results
from Filtering.filtering import company_finding 
from Sentimentanalysis.sentimentanalysis import sentiment_analysis , sentiment_formatter 
from Predictions_util.predictions_util import predictions ,technical_indct ,  cmp_volume ,format_value

import yfinance as yf

import time
import pandas as pd
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from aiojobs import create_scheduler

app = FastAPI()

async def update():
    while True:

        print("Update called...**************")

        # df = combine_dfs(economictimes(),moneycontrol(),investing(),livemint(),businesstoday(),cnbc(),zeebiz())
        df = scrape_news()

        save_news(df) 



        df = company_finding(df)




        print(f"Collected from News {df}")



        df = df[df["Mentions"] >= 3 ]

        print(f"Before Filtering{df}")
        print("###########")

        df = filter_old_ticker(df) #filters repetaions if repeated agian before 3 weeks 
        print(f"After Filtering {df}")


        
        if not df.empty:
            df = sentiment_analysis(df)
            # df = sentiment_analysis_LLAMA(df)


        print(df)

        if not df.empty:    
            df = predictions(df)
            
        if df.empty:
            print("No Prediction from predictions function")
        print(df)
        df = precomputed(df)
        df = filter_old_ticker(df)



        if not df.empty:
            df = technical_indct(df)
            save_predictions(df)


        await asyncio.sleep(600)  

@app.on_event("startup")
async def startup_event():
    scheduler = await create_scheduler()
    await scheduler.spawn(update())
