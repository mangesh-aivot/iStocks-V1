import pandas as pd
import re
import os

def company_finding(df):
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir,'..','Data','NSE Data','MCAP28032024.xlsx')
    nse = pd.read_excel(path)
    # nse = pd.read_excel(r'C:\Users\ASUS\Projects\UI\StockApp\backend\Predictions\Data\NSE Data\MCAP28032024.xlsx')


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
