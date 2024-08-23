gemini_key_1 = 'AIzaSyAwl6TV5TFIfBHnYGFvB2hSox02dyk0r24'
gemini_key_2 = 'AIzaSyDXy8fhn-S8T83idEqhTn2zARlIZjQcjes'

from fastapi import FastAPI
import google.generativeai as genai
from bs4 import BeautifulSoup
import requests
from dateutil import parser
import datetime
import time
from datetime import date
import pandas as pd
from pandas.errors import EmptyDataError
import numpy as np
from datetime import datetime
import yfinance as yf
from datetime import datetime, timedelta
import glob
import re
from pytz import timezone
import pytz
import time 
import concurrent.futures
import textwrap
from fastapi.middleware.cors import CORSMiddleware
from tradingview_ta import TA_Handler, Interval, Exchange
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dateutil import parser

app = FastAPI()
origins = [
    "http://localhost:5173",  # Add your frontend URL here
    # "http://192.168.1.139:5173/prediction"
    # Add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def economictimes():

    headlines = []
    summaries = []
    dates = []

    ET_link = 'https://economictimes.indiatimes.com/markets/stocks/news'
    base_url = ET_link

    response = requests.get(base_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('div', class_='eachStory')

    for article in articles:
        headline_element = article.find('h3').find('a')
        headline = headline_element.text.strip() if headline_element else None

        summary_element = article.find('p')
        summary = summary_element.text.strip() if summary_element else None

        timestamp_element = article.find('time')
        timestamp_text = timestamp_element.text.strip() if timestamp_element else None

        if timestamp_text:
            timestamp_text = timestamp_text.replace('IST', '+0530')

            date = parser.parse(timestamp_text).strftime('%Y-%m-%d')
        else:
            date = None

        headlines.append(headline)
        summaries.append(summary)
        dates.append(date)

    ET_df = pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})
    return ET_df

def moneycontrol():

    MC_link1 = 'https://www.moneycontrol.com/news/business/companies/'

    headlines = []
    summaries = []
    dates = []

    response = requests.get(MC_link1)

    soup = BeautifulSoup(response.content,'html.parser')

    news_items = soup.find_all('li',class_='clearfix')


    for item in news_items:

        title = item.find('h2').text.strip()


        paragraphs = item.find_all('p')
        paragraph_text = ' '.join([p.text.strip() for p in paragraphs])


        time_string = item.find('span').text.strip()
        time_string = time_string.replace(' IST', '')
        time_object = datetime.strptime(time_string, "%B %d, %Y %I:%M %p")
        time_ = time_object.strftime('%Y-%m-%d')

        headlines.append(title)
        summaries.append(paragraph_text)
        dates.append(time_)

    MC_df1 = pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})




    MC_link2 = 'https://www.moneycontrol.com/news/business/stocks/'
    headlines = []
    summaries = []
    dates = []

    response = requests.get(MC_link2)

    soup = BeautifulSoup(response.content,'html.parser')

    news_items = soup.find_all('li',class_='clearfix')


    for item in news_items:

        title = item.find('h2').text.strip()


        paragraphs = item.find_all('p')
        paragraph_text = ' '.join([p.text.strip() for p in paragraphs])


        time_string = item.find('span').text.strip()
        time_string = time_string.replace(' IST', '')
        time_object = datetime.strptime(time_string, "%B %d, %Y %I:%M %p")
        time_ = time_object.strftime('%Y-%m-%d')

        headlines.append(title)
        summaries.append(paragraph_text)
        dates.append(time_)

    MC_df2 = pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})

    MC_df = pd.concat([MC_df1,MC_df2],axis=0)

    MC_df.drop_duplicates(inplace=True)

    MC_df.reset_index(drop=True, inplace=True)
    return MC_df


def investing():

    INV_link = 'https://in.investing.com/news/markets/stock-market/'
    headlines = []
    summaries = []
    dates = []

    base_url = INV_link

    num_pages = 4

    for page_num in range(1, num_pages + 1):
        url = f'{base_url}{page_num}'

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('li', class_='common-articles-item')

        for article in articles:
            headline_element = article.find('h3', class_='title')
            headline = headline_element.text.strip() if headline_element else None

            summary_element = article.find('p', class_='summery')
            summary = summary_element.text.strip() if summary_element else None

            timestamp_element = article.find('time', class_='js-comment-time')
            timestamp = timestamp_element.get('data-timestamp') if timestamp_element else None

            date = None
            if timestamp:
                timestamp = int(timestamp)
                date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            headlines.append(headline)
            summaries.append(summary)
            dates.append(date)

    INV_df = pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})
    return INV_df

def livemint():
    base_url = "https://www.livemint.com/market/stock-market-news/page-"
    data = []

    for page_num in range(1, 6):  # Scraping pages 1 to 5
        url = base_url + str(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for div in soup.find_all('div', class_='listingNew'):
            date = div.find('span', {'id': lambda x: x and x.startswith('tListBox_')}).text
            headline = div.find('h2', class_='headline').text.strip()
            img_elem = div.find('a').find('img')
            summary = img_elem['title'] if img_elem and 'title' in img_elem.attrs else ''
            data.append({'Date': date, 'Headline': headline, 'Summary': summary})

    Mint_df = pd.DataFrame(data)
    return Mint_df

def businesstoday():

    url = "https://www.businesstoday.in/markets/company-stock"


    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    section_listing = soup.find("div", class_="section-listing-LHS")

    data = {'Headline': [], 'Summary': [], 'Date': []}

    if section_listing:
        widget_listings = section_listing.find_all("div", class_="widget-listing")

        for widget_listing in widget_listings:
            paragraphs = widget_listing.find_all("p")
            headers = widget_listing.find_all("h2")
            times = widget_listing.find_all("span")

            for time, header, paragraph in zip(times, headers, paragraphs):
                date_str = time.text.strip().split(": ")[1]  # Extracting date string
                date_obj = datetime.strptime(date_str, "%b %d, %Y")  # Converting to datetime object
                formatted_date = date_obj.strftime("%Y-%m-%d")

                data['Date'].append(formatted_date)
                data['Headline'].append(header.text.strip())
                data['Summary'].append(paragraph.text.strip())
    BT_df = pd.DataFrame(data)
    return BT_df

def cnbc():
    url = 'https://www.cnbctv18.com/market/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    section = soup.find('section', class_='jsx-42d95dab3970c9b7 mrkt-top-widget common-mkt-css')

    h3_texts = [h3.get_text() for h3 in section.find_all('h3')]

    div_texts = [div.get_text() for div in section.find_all('div', class_='jsx-42d95dab3970c9b7 mkt-ts')]

    def convert_date(date_str):
        date_part = ' '.join(date_str.split()[:3])
        date_obj = datetime.strptime(date_part, '%b %d, %Y')
        return date_obj.strftime('%Y-%m-%d')

    formatted_dates = [convert_date(date) for date in div_texts]

    CNBC_df = pd.DataFrame({"Headline": h3_texts,"Summary":h3_texts, "Date": formatted_dates})
    return CNBC_df

def zeebiz():

    url = "https://www.zeebiz.com/markets/stocks"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    h3_tags = soup.find_all('h3')

    headlines = []
    links = []
    details = []

    for h3 in h3_tags:
        for a in h3.find_all('a'):
            headlines.append(a.get_text(strip=True))
            links.append(a.get('href'))

    # For each link, navigating to the linked page and extracting the  Summary
    for link in links:
        try:
            link = "https://www.zeebiz.com" + link
            detail_response = requests.get(link)
            detail_response.raise_for_status()
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
            detail_tag = detail_soup.find('h2', class_='biz-a-sum')
            if detail_tag:
                details.append(detail_tag.get_text(strip=True))
            else:
                details.append("N/A")
        except:
            details.append("N/A")

    ZEEBIZ_df = pd.DataFrame({
        "Headline": headlines,
        "Summary":details
    })

    ZEEBIZ_df.drop_duplicates(inplace=True)
    return ZEEBIZ_df

def combine_dfs(*dfs):
    df = pd.concat(dfs,axis=0)
    df.drop_duplicates(inplace=True)
    df = df.reset_index(drop=True)
    return df

def company_finding(df):

    nse = pd.read_excel(r'C:\Users\ASUS\Projects\UI\StockApp\backend\Predictions\Data\NSE Data\MCAP28032024.xlsx')

    nse.dropna(subset=['Company Name'], inplace=True)
    nse['Company Name'] = nse['Company Name'].str.replace(' Limited', '', regex=False)
    company_info = dict(zip(nse['Company Name'], nse['Symbol']))

    company_headlines = {name: [] for name in company_info.keys()}
    company_summaries = {name: [] for name in company_info.keys()}

    for index, row in df.iterrows():
        headline = row['Headline']
        summary = row['Summary']

        if isinstance(summary, str):
            words = re.findall(r'\b\w+\b', summary.lower())
            for company in company_info.keys():
                company_words = company.lower().split()

                for i in range(len(words) - len(company_words) + 1):
                    if words[i:i + len(company_words)] == company_words:
                        company_headlines[company].append(headline)
                        company_summaries[company].append(summary)
                        break

    total_companies_with_mentions = sum(1 for headlines in company_headlines.values() if headlines)

    sorted_companies = sorted(company_summaries.items(), key=lambda x: len(x[1]), reverse=True)


    companies = []
    symbols = []
    mentions = []
    summaries = []

    for company, summary in sorted_companies:
        companies.append(company)
        symbols.append(company_info[company])
        mentions.append(len(summary))

        summary_str = '", "'.join(summary)
        summaries.append(f'"{summary_str}"')

    df = pd.DataFrame({
        'Company Name': companies,
        'Company Symbol': symbols,
        'Mentions': mentions,
        'Summaries': summaries #news 
    })
    return df

def save_news(df):
    utc_now = datetime.now(pytz.utc)

    # Convert to IST
    ist = timezone('Asia/Kolkata')
    ist_now = utc_now.astimezone(ist)
    current_date_ist = ist_now.strftime('%Y-%m-%d')
    current_time_ist = ist_now.strftime('%I-%M%p')

    file_name = f"News_on_{current_date_ist}_at_{current_time_ist}"
    # saving the news 
    df.to_csv(df.to_csv(f'C:/Users/ASUS/Projects/UI/StockApp/backend/Predictions/Data/News/{file_name}.csv'))



def sentiment_analysis(df):
    print("sentiment_analysis - 1")

    genai.configure(api_key=gemini_key_1)


    model = genai.GenerativeModel('gemini-1.0-pro-latest')



    df['Sentiment'] = ''


    for index,row in df.iterrows():
        text = row['Summaries']
        company = row['Company Name']
        prompt = f"Please analyse these news headlines and give sentiment score between -1 to +1 (ex like  1,0.8, 0.3,-0.5,-0.8,-1 etc) to {company} company based on the stock market news. Sum those sentiment scores to give the net sentiment value of that company . The ouput should only contain the net sentiment value , with no additional commentry , explanation or extra information ."  + " Please process the following headlines: " + text

        response = model.generate_content(prompt)

        df.loc[index, 'Sentiment'] = response.text


    df = df[df['Company Name'] != 'BSE']


    df['Sentiment'] = df['Sentiment'].astype(str).astype(float)


    df = df[df['Sentiment'] >= 1 ]
    print("sentiment_analysis - 2")
    print(df)
    return df

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1wk')
    return stock_data

def calculate_pivot_points(data):
    data['PP'] = (data['High'] + data['Low'] + data['Close']) / 3
    data['R1'] = (2 * data['PP']) - data['Low']
    data['R2'] = data['PP'] + (data['High'] - data['Low'])
    data['R3'] = data['High'] + 2 * (data['PP'] - data['Low'])
    return data
def format_value(value):
    if value < 100:
        return f"{value:.2f}"
    else:
        return f"{value:.0f}"

def today_price(ticker):
    ticker = yf.Ticker(ticker)
    current_price = ticker.history(period='1d')['Close'][0]
    return current_price

def company_fundamentals(company_symbol):
    count = 0
    url = f'https://www.screener.in/company/{company_symbol}/#profit-loss'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ###### Profit & Loss #####
    table1 = soup.find("section", id="profit-loss")

    header = [th.text.strip() for th in table1.find("thead").find_all("th")]

    data1 = []
    rows = table1.find("tbody").find_all("tr")
    for row in rows:
        cols = [col.text.strip() if col.text.strip() != '--' else np.nan for col in row.find_all(["td", "th"])]
        data1.append(cols)

    df1 = pd.DataFrame(data1, columns=header)
    ##
    df1.columns = ["Parameters"] + list(df1.columns[1:])
    ##
    print(df1)
    sales_last_q = float(df1[df1['Parameters'] == 'Sales\xa0+'][df1.columns[-1]].iloc[0].replace(',', '').strip())
    sales_3rdlast_q = float(df1[df1['Parameters'] == 'Sales\xa0+'][df1.columns[-3]].iloc[0].replace(',', '').strip())
    net_profit_last_q = float(df1[df1['Parameters'] == 'Net Profit\xa0+'][df1.columns[-1]].iloc[0].replace(',', '').strip())
    net_profit_3rdlast_q = float(df1[df1['Parameters'] == 'Net Profit\xa0+'][df1.columns[-3]].iloc[0].replace(',', '').strip())
    eps_last_q = float(df1[df1['Parameters'] == 'EPS in Rs'][df1.columns[-1]].iloc[0].replace(',', '').strip())
    eps_3rdlast_q = float(df1[df1['Parameters'] == 'EPS in Rs'][df1.columns[-3]].iloc[0].replace(',', '').strip())

    if sales_last_q > sales_3rdlast_q:
        count+=1
    if net_profit_last_q > net_profit_3rdlast_q:
        count+=1
    if eps_last_q > eps_3rdlast_q:
        count+=1
    ######  Balance Sheet ######
    balance_sheet_section = soup.find("section", id="balance-sheet")

    table2 = balance_sheet_section.find("table")

    header = [th.text.strip() for th in table2.find("thead").find_all("th")]
    data2 = []
    rows = table2.find("tbody").find_all("tr")
    for row in rows:
        cols = [col.text.strip() if col.text.strip() != '--' else pd.NA for col in row.find_all(["td", "th"])]
        data2.append(cols)
    df2 = pd.DataFrame(data2, columns=header)
    ##
    df2.columns = ["Parameters"] + list(df2.columns[1:])
    ##
    print(df2)
    reserves_last_q = float(df2[df2['Parameters'] == 'Reserves'][df2.columns[-1]].iloc[0].replace(',', '').strip())
    reserves_3rdlast_q = float(df2[df2['Parameters'] == 'Reserves'][df2.columns[-3]].iloc[0].replace(',', '').strip())
    total_assets_last_q = float(df2[df2['Parameters'] == 'Reserves'][df2.columns[-1]].iloc[0].replace(',', '').strip())
    total_assets_3rdlast_q = float(df2[df2['Parameters'] == 'Reserves'][df2.columns[-3]].iloc[0].replace(',', '').strip())

    if reserves_last_q > reserves_3rdlast_q:
        count+=1
    if total_assets_last_q > total_assets_3rdlast_q:
        count+=1
    #### Cash Flow ####
    cash_flow_section = soup.find("section", id="cash-flow")

    table3 = cash_flow_section.find("table")

    header = [th.text.strip() for th in table3.find("thead").find_all("th")]
    data3 = []
    rows = table3.find("tbody").find_all("tr")
    for row in rows:
        cols = [col.text.strip() if col.text.strip() != '--' else pd.NA for col in row.find_all(["td", "th"])]
        data3.append(cols)

    df3 = pd.DataFrame(data3, columns=header)
    ##
    df3.columns = ["Parameters"] + list(df3.columns[1:])
    ##
    print(df3)
    cash_flow_from_operating_activities_last_q = float(df3[df3['Parameters'] == 'Cash from Operating Activity\xa0+'][df3.columns[-1]].iloc[0].replace(',', '').strip())
    cash_flow_from_operating_activities_3rdlast_q = float(df3[df3['Parameters'] == 'Cash from Operating Activity\xa0+'][df3.columns[-3]].iloc[0].replace(',', '').strip())

    if cash_flow_from_operating_activities_last_q > cash_flow_from_operating_activities_3rdlast_q:
        count+=1
    ###### Piotrosky #####
    login_url = 'https://www.screener.in/login/'
    username = 'saptarshi@aivot.ai'
    password = '123aivot'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)

    # Perform login
    driver.get(login_url)
    username_field = driver.find_element(By.ID, 'id_username')
    password_field = driver.find_element(By.ID, 'id_password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    url_ = url

    time.sleep(1)  # Adjust sleep time if necessary
    driver.get(url_)
    time.sleep(1)  # Ensure the page is fully loaded

    html_content = driver.page_source

    soup_ = BeautifulSoup(html_content, 'html.parser')

    piotroski_li = soup_.find('li', class_='flex flex-space-between', attrs={'data-source': 'quick-ratio'})
    piotroski_score = None

    for li in soup_.find_all('li', class_='flex flex-space-between', attrs={'data-source': 'quick-ratio'}):
        if li.find('span', class_='name').text.strip() == 'Piotroski score':
            piotroski_score = float(li.find('span', class_='number').text.strip())
            break
    count += piotroski_score
    # print(f"Piotroski score: {piotroski_score}")
    driver.quit()
    print(f'Count: {count}')
    if count > 10:
        return 'Strong'
    elif 6 <= count <= 10 :
        return 'Stable'
    elif count < 6:
        return 'Weak'


def predictions(df):
    print("Entered the predictions function")
    end_date = datetime.today()

    start_date = end_date - timedelta(days=7)

    # Adjust start date if it falls on a weekend
    if start_date.weekday() == 5:  # Saturday
        start_date = start_date - timedelta(days=1)
    elif start_date.weekday() == 6:  # Sunday
        start_date = start_date - timedelta(days=2)

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')


    results = []

    for index, row in df.iterrows():
        company_name = row['Company Name']
        company_symbol = row['Company Symbol']
        news = row['Summaries']
        sentiment = row['Sentiment']
        ticker = company_symbol + '.NS'


        stock_data = get_stock_data(ticker, start_date, end_date)
        if not stock_data.empty:
            stock_data = calculate_pivot_points(stock_data)
            tp_values = stock_data.iloc[-1]

            cmp_val = today_price(ticker)
            tp = format_value(tp_values['R1'])
            print(f"CMP -- {cmp_val}")
            tp = float(tp)
            profit = tp - cmp_val
            print(f"Profit -- {profit}")
            if profit < 0:
                continue
            sl = cmp_val - (profit/2)
            print(f"SL -- {sl}")

            b_lower = cmp_val - (cmp_val*.02)
            b_lower = format_value(b_lower)

            b_upper = cmp_val + (cmp_val*.02)
            b_upper = format_value(b_upper)


            results.append({
                'Company Name': company_name,
                'Company Symbol': company_symbol,
                'Buy at': cmp_val,
                'TP1': format_value(tp_values['R1']),
                'TP2': format_value(tp_values['R2']),
                'TP3': format_value(tp_values['R3']),
                'SL' : format_value(sl),
                'Buy at': f"{b_lower}-{b_upper}",
                'Time': '0-3 Weeks',
                'News': news,
                'Sentiment':sentiment,
                'Fundamental':company_fundamentals(company_symbol)
            })
    results_df = pd.DataFrame(results)
    print("Done ---- predictions function")

    return results_df 


def save_predictions(results_df):
    utc_now = datetime.now(pytz.utc)

    # Convert to IST
    ist = timezone('Asia/Kolkata')
    ist_now = utc_now.astimezone(ist)
    current_date_ist = ist_now.strftime('%Y-%m-%d')
    current_time_ist = ist_now.strftime('%I-%M%p')

    # Define folder path
    folder_path = "C:\\Users\\ASUS\\Projects\\UI\\StockApp\\backend\\Predictions\\Data\\Results"


    
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

def technical_indct(df):
    df['Technical'] = ''
    for index, row in df.iterrows():
        ticker = row['Company Symbol']
        tesla = TA_Handler(
            symbol=ticker,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_WEEK
        )

        df.at[index,'Technical'] = tesla.get_analysis().summary['RECOMMENDATION']
    return df


def cmp_volume(df):
    df['CMP']= np.nan
    df['Volume']= np.nan
    for index, row in df.iterrows():
        ticker = row['Company Symbol']

        ticker = ticker + '.NS'
        stock = yf.Ticker(ticker)

        live_data = stock.history(period='1d', interval='1d') #1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

        latest_data = live_data.iloc[-1]

        df.at[index,'CMP'] = format_value(latest_data['Close'])
        df.at[index,'Volume'] = int(latest_data['Volume'])
    return df


def combine_results():

    folder_path = 'C:/Users/ASUS/Projects/UI/StockApp/backend/Predictions/Data/Results'

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

    final_df = combined_df.drop_duplicates(subset=['Company Symbol'], keep='first')

    combined_df = combined_df.sort_values(by='Date')


    return final_df

def filter_old_ticker(df2):
    df1 = combine_results()
    # Ensure the 'Date' column in df1 is in datetime format
    df1['Date'] = pd.to_datetime(df1['Date'])
    
    # Get today's date
    today = datetime.now()
    
    # Calculate the threshold date (3 weeks ago)
    threshold_date = today - timedelta(weeks=3)
    
    # Function to check if a ticker should be kept in df2
    def should_keep_ticker(ticker):
        # Check if the ticker is in df1
        if ticker in df1['Company Symbol'].values:
            # Get the date(s) associated with this ticker in df1
            dates = df1[df1['Company Symbol'] == ticker]['Date']
            # Check if any of the dates are within the last 3 weeks
            if any(dates > threshold_date):
                return False
        return True
    
    # Apply the function to filter df2
    df2_filtered = df2[df2['Company Symbol'].apply(should_keep_ticker)]
    
    return df2_filtered




def precomputed(df):
    folder_path = "C:\\Users\\ASUS\\Projects\\UI\\StockApp\\backend\\Predictions\\Data\\Results"


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




@app.get("/")
def home():
    return {"Message":"Hello"}

@app.get("/get-predictions")
def get_prediction():

    df = combine_dfs(economictimes(),moneycontrol(),investing(),livemint(),businesstoday(),cnbc(),zeebiz())
    # df = combine_dfs(economictimes(),moneycontrol(),investing(),livemint(),businesstoday(),cnbc())

    df = company_finding(df)

    print(f"Collected from News {df}")
    save_news(df) 


    df = df[df["Mentions"] >= 3 ]

    print(f"Before Filtering{df}")
    print("###########")

    df = filter_old_ticker(df) #filters repetaions if repeated agian before 3 weeks 
    print(f"After Filtering {df}")

    
    if not df.empty:
        df = sentiment_analysis(df)


    print(df)

    if not df.empty:    
        df = predictions(df)
    if df.empty:
        print("No Prediction from predictions function")
    print(df)
    df = precomputed(df)
    df = filter_old_ticker(df)

    if not df.empty:
        save_predictions(df)
    # df = pd.read_csv('/home/rahul-/Projects/UI/StockApp/backend/Data/Results/Predictions_on_2024-06-26_at_12-59PM.csv')
    # print(df)
    if df.empty:
        return {"Message":"No prediction for Today"}
    

    # df = pd.read_csv(r'C:\Users\ASUS\Projects\UI\StockApp\backend\Data\Results\Predictions_on_2024-07-09_at_10-50AM.csv')
    df = cmp_volume(df)
    df = technical_indct(df)

    df = df.fillna('')

    predictions_df = df.to_dict(orient='records')
    # predictions_df = [{'Unnamed: 0': 0, 'Company Name': 'Trent', 'Company Symbol': 'TRENT', 'TP1': 5038, 'TP2': 5106, 'TP3': 5165,'SL':4966,'Time':'0-3 Weeks','CMP':4990,'Volume':33546,'Technical':'Strong Buy'}]
    return  predictions_df


