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




def economictimes():
    headlines = []
    summaries = []
    dates = []

    ET_link = 'https://economictimes.indiatimes.com/markets/stocks/news'
    base_url = ET_link

    try:
        response = requests.get(base_url)
        response.raise_for_status() 
    except requests.RequestException as e:
        print(f"Error fetching data from {base_url}: {e}")
        return pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_='eachStory')

        for article in articles:
            try:
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
            except Exception as e:
                print(f"Error processing article: {e}")
                continue

    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})

    ET_df = pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})
    return ET_df


def moneycontrol():
    MC_link1 = 'https://www.moneycontrol.com/news/business/companies/'
    MC_link2 = 'https://www.moneycontrol.com/news/business/stocks/'

    def fetch_data(url):
        headlines = []
        summaries = []
        dates = []

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = soup.find_all('li', class_='clearfix')

            for item in news_items:
                try:
                    title = item.find('h2').text.strip() if item.find('h2') else None

                    paragraphs = item.find_all('p')
                    paragraph_text = ' '.join([p.text.strip() for p in paragraphs])

                    time_string = item.find('span').text.strip() if item.find('span') else None
                    if time_string:
                        time_string = time_string.replace(' IST', '')
                        time_object = datetime.strptime(time_string, "%B %d, %Y %I:%M %p")
                        time_ = time_object.strftime('%Y-%m-%d')
                    else:
                        time_ = None

                    headlines.append(title)
                    summaries.append(paragraph_text)
                    dates.append(time_)
                except Exception as e:
                    print(f"Error processing news item: {e}")
                    continue

        except Exception as e:
            print(f"Error parsing HTML content from {url}: {e}")
            return pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})

        return pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})

    MC_df1 = fetch_data(MC_link1)
    MC_df2 = fetch_data(MC_link2)

    MC_df = pd.concat([MC_df1, MC_df2], axis=0)

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

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            continue

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('li', class_='common-articles-item')

            for article in articles:
                try:
                    headline_element = article.find('h3', class_='title')
                    headline = headline_element.text.strip() if headline_element else None

                    summary_element = article.find('p', class_='summery')
                    summary = summary_element.text.strip() if summary_element else None

                    timestamp_element = article.find('time', class_='js-comment-time')
                    timestamp = timestamp_element.get('data-timestamp') if timestamp_element else None

                    date = None
                    if timestamp:
                        timestamp = int(timestamp)
                        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

                    headlines.append(headline)
                    summaries.append(summary)
                    dates.append(date)
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue

        except Exception as e:
            print(f"Error parsing HTML content from {url}: {e}")
            continue

    INV_df = pd.DataFrame({'Headline': headlines, 'Summary': summaries, 'Date': dates})
    return INV_df


import requests
from bs4 import BeautifulSoup
import pandas as pd

def livemint():
    base_url = "https://www.livemint.com/market/stock-market-news/page-"
    data = []

    for page_num in range(1, 6):  # Scraping pages 1 to 5
        url = base_url + str(page_num)
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            continue

        try:
            soup = BeautifulSoup(response.content, 'html.parser')

            for div in soup.find_all('div', class_='listingNew'):
                try:
                    date_element = div.find('span', {'id': lambda x: x and x.startswith('tListBox_')})
                    date = date_element.text.strip() if date_element else None

                    headline_element = div.find('h2', class_='headline')
                    headline = headline_element.text.strip() if headline_element else None

                    img_elem = div.find('a').find('img')
                    summary = img_elem['title'] if img_elem and 'title' in img_elem.attrs else ''

                    data.append({'Date': date, 'Headline': headline, 'Summary': summary})
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue

        except Exception as e:
            print(f"Error parsing HTML content from {url}: {e}")
            continue

    Mint_df = pd.DataFrame(data)
    return Mint_df


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def businesstoday():
    url = "https://www.businesstoday.in/markets/company-stock"
    data = {'Headline': [], 'Summary': [], 'Date': []}

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return pd.DataFrame(data)

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        section_listing = soup.find("div", class_="section-listing-LHS")

        if section_listing:
            widget_listings = section_listing.find_all("div", class_="widget-listing")

            for widget_listing in widget_listings:
                paragraphs = widget_listing.find_all("p")
                headers = widget_listing.find_all("h2")
                times = widget_listing.find_all("span")

                for time, header, paragraph in zip(times, headers, paragraphs):
                    try:
                        date_str = time.text.strip().split(": ")[1]  # Extracting date string
                        date_obj = datetime.strptime(date_str, "%b %d, %Y")  # Converting to datetime object
                        formatted_date = date_obj.strftime("%Y-%m-%d")

                        data['Date'].append(formatted_date)
                        data['Headline'].append(header.text.strip())
                        data['Summary'].append(paragraph.text.strip())
                    except Exception as e:
                        print(f"Error processing article: {e}")
                        continue

    except Exception as e:
        print(f"Error parsing HTML content from {url}: {e}")
        return pd.DataFrame(data)

    BT_df = pd.DataFrame(data)
    return BT_df




def cnbc():
    url = 'https://www.cnbctv18.com/market/'
    data = {"Headline": [], "Summary": [], "Date": []}

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return pd.DataFrame(data)

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        section = soup.find('section', class_='jsx-42d95dab3970c9b7 mrkt-top-widget common-mkt-css')

        if section:
            h3_texts = [h3.get_text() for h3 in section.find_all('h3')]
            div_texts = [div.get_text() for div in section.find_all('div', class_='jsx-42d95dab3970c9b7 mkt-ts')]

            def convert_date(date_str):
                try:
                    date_part = ' '.join(date_str.split()[:3])
                    date_obj = datetime.strptime(date_part, '%b %d, %Y')
                    return date_obj.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"Error converting date: {e}")
                    return None

            formatted_dates = [convert_date(date) for date in div_texts]

            data["Headline"] = h3_texts
            data["Summary"] = h3_texts
            data["Date"] = formatted_dates
        else:
            print(f"Section with class 'jsx-42d95dab3970c9b7 mrkt-top-widget common-mkt-css' not found in {url}")
            return pd.DataFrame(data)

    except Exception as e:
        print(f"Error parsing HTML content from {url}: {e}")
        return pd.DataFrame(data)

    CNBC_df = pd.DataFrame(data)
    return CNBC_df



def zeebiz():
    url = "https://www.zeebiz.com/markets/stocks"
    headlines = []
    links = []
    details = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return pd.DataFrame({"Headline": headlines, "Summary": details})

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        h3_tags = soup.find_all('h3')

        for h3 in h3_tags:
            for a in h3.find_all('a'):
                headlines.append(a.get_text(strip=True))
                links.append(a.get('href'))

        # For each link, navigate to the linked page and extract the summary
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
            except requests.RequestException as e:
                print(f"Error fetching details from {link}: {e}")
                details.append("N/A")
            except Exception as e:
                print(f"Error parsing details from {link}: {e}")
                details.append("N/A")

    except Exception as e:
        print(f"Error parsing HTML content from {url}: {e}")
        return pd.DataFrame({"Headline": headlines, "Summary": details})

    ZEEBIZ_df = pd.DataFrame({
        "Headline": headlines,
        "Summary": details
    })

    ZEEBIZ_df.drop_duplicates(inplace=True)
    return ZEEBIZ_df




def combine_dfs(*dfs):
    df = pd.concat(dfs,axis=0)
    df.drop_duplicates(inplace=True)
    df = df.reset_index(drop=True)
    return df


def scrape_news():
    df = combine_dfs(economictimes(),moneycontrol(),livemint(),businesstoday(),cnbc(),zeebiz())
    return df;