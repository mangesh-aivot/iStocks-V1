import pandas as pd
import yfinance as yf
import numpy as np
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
from tradingview_ta import TA_Handler, Interval, Exchange

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
    try:
        count = 0
        url = f'https://www.screener.in/company/{company_symbol}/#profit-loss'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        ###### Profit & Loss #####
        table1 = soup.find("section", id="profit-loss")

        header = [th.text.strip() for th in table1.find("thead").find_all("th")]
        rows = table1.find("tbody").find_all("tr")

        data1 = []
        for row in rows:
            cols = [col.text.strip() if col.text.strip() != '--' else np.nan for col in row.find_all(["td", "th"])]
            data1.append(cols)
            
        df1 = pd.DataFrame(data1, columns=header)
        ##
        df1.columns = ["Parameters"] + list(df1.columns[1:])
        
        def get_value(df, primary_param, secondary_param, column_index):
            filtered_df = df[df['Parameters'] == primary_param]
            if not filtered_df.empty:
                value = float(filtered_df[df.columns[column_index]].iloc[0].replace(',', '').strip())
            else:
                filtered_df = df[df['Parameters'] == secondary_param]
                if not filtered_df.empty:
                    value = float(filtered_df[df.columns[column_index]].iloc[0].replace(',', '').strip())
                else:
                    value = np.nan
            return value

        # Parameters
        primary_sales_param = 'Sales\xa0+'
        secondary_sales_param = 'Revenue'
        primary_net_profit_param = 'Net Profit\xa0+'
        primary_eps_param = 'EPS in Rs'

        # Get values
        sales_last_q = get_value(df1, primary_sales_param, secondary_sales_param, -1)
        sales_3rdlast_q = get_value(df1, primary_sales_param, secondary_sales_param, -3)
        net_profit_last_q = get_value(df1, primary_net_profit_param, primary_net_profit_param, -1)
        net_profit_3rdlast_q = get_value(df1, primary_net_profit_param, primary_net_profit_param, -3)
        eps_last_q = get_value(df1, primary_eps_param, primary_eps_param, -1)
        eps_3rdlast_q = get_value(df1, primary_eps_param, primary_eps_param, -3)
        # for row in rows:
        #     cols = [col.text.strip() if col.text.strip() != '--' else np.nan for col in row.find_all(["td", "th"])]
        #     data1.append(cols)

        # df1 = pd.DataFrame(data1, columns=header)
        # ##
        # df1.columns = ["Parameters"] + list(df1.columns[1:])
        # ##
    
        # sales_last_q = float(df1[df1['Parameters'] == 'Sales\xa0+'][df1.columns[-1]].iloc[0].replace(',', '').strip())
        # sales_3rdlast_q = float(df1[df1['Parameters'] == 'Sales\xa0+'][df1.columns[-3]].iloc[0].replace(',', '').strip())
        # net_profit_last_q = float(df1[df1['Parameters'] == 'Net Profit\xa0+'][df1.columns[-1]].iloc[0].replace(',', '').strip())
        # net_profit_3rdlast_q = float(df1[df1['Parameters'] == 'Net Profit\xa0+'][df1.columns[-3]].iloc[0].replace(',', '').strip())
        # eps_last_q = float(df1[df1['Parameters'] == 'EPS in Rs'][df1.columns[-1]].iloc[0].replace(',', '').strip())
        # eps_3rdlast_q = float(df1[df1['Parameters'] == 'EPS in Rs'][df1.columns[-3]].iloc[0].replace(',', '').strip())

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
        reserves_last_q = float(df2[df2['Parameters'] == 'Reserves'][df2.columns[-1]].iloc[0].replace(',', '').strip())
        reserves_3rdlast_q = float(df2[df2['Parameters'] == 'Reserves'][df2.columns[-3]].iloc[0].replace(',', '').strip())
        total_assets_last_q = float(df2[df2['Parameters'] == 'Total Assets'][df2.columns[-1]].iloc[0].replace(',', '').strip())
        total_assets_3rdlast_q = float(df2[df2['Parameters'] == 'Total Assets'][df2.columns[-3]].iloc[0].replace(',', '').strip())

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
        driver.quit()

        if count > 10:
            return 'Strong'
        elif 6 <= count <= 10 :
            return 'Stable'
        elif count < 6:
            return 'Weak'
    except Exception as e :
        print(f"Error occured: {e}")
        return 'No Data'
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


def technical_indct(df):
    df['Technical'] = ''
    try:
        for index, row in df.iterrows():
            ticker = row['Company Symbol']
            tesla = TA_Handler(
                symbol=ticker,
                screener="india",
                exchange="NSE",
                interval=Interval.INTERVAL_1_WEEK
            )

            df.at[index, 'Technical'] = tesla.get_analysis().summary['RECOMMENDATION']
    except Exception as e:
        print(f"Error for ticker {ticker}: {e}")
        df.at[index, 'Technical'] = "No Data"
    
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
