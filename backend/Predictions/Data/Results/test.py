import os
import pandas as pd
from datetime import datetime
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


economictimes_df = economictimes()
moneycontrol_df = moneycontrol()
investing_df = investing()
livemint_df = livemint()
businesstoday_df = businesstoday()
cnbc_df = cnbc()
# zeebiz_df = zeebiz()
# df = combine_dfs(economictimes_df,moneycontrol_df,investing_df,livemint_df,businesstoday_df,cnbc_df,zeebiz_df)
df = combine_dfs(economictimes_df,moneycontrol_df,investing_df,livemint_df,businesstoday_df,cnbc_df)



nse = pd.read_excel(r'C:\Users\ASUS\Projects\UI\StockApp\backend\Data\NSE Data\MCAP28032024.xlsx')

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

print(df)
