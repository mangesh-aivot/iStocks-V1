gemini_key_1 = 'AIzaSyAwl6TV5TFIfBHnYGFvB2hSox02dyk0r24'
gemini_key_2 = 'AIzaSyDXy8fhn-S8T83idEqhTn2zARlIZjQcjes'
gemini_key_3  = 'AIzaSyBvndA4ucYOF8BMZoDBirKCHquSbCEzqTE'
 
import google.generativeai as genai
import time 
import re

def sentiment_analysis(df):
    print("sentiment_analysis - 1")

    genai.configure(api_key=gemini_key_3)


    model = genai.GenerativeModel('gemini-1.0-pro-latest')



    df['Sentiment'] = ''


    for index,row in df.iterrows():
        try :
            text = row['Summaries']
            company = row['Company Name']
            prompt = f"Please analyse these news headlines and give sentiment score between -1 to +1 (ex like  1,0.8, 0.3,-0.5,-0.8,-1 etc) to {company} company based on the stock market news. Sum those sentiment scores to give the net sentiment value of that company . The ouput should only contain the net sentiment value , with no additional commentry , explanation or extra information ."  + " Please process the following headlines: " + text

            time.sleep(3)

            response = model.generate_content(prompt)

            pattern = r'-?\d+\.\d+|-?\d+'
            match = re.search(pattern, response.text)
            df.loc[index, 'Sentiment'] = float(match.group())

        except Exception as e:
            print(f"Error during sentiment analysis at index {index}, company {company}: {e}")

    try :
        df = df[df['Company Name'] != 'BSE']


        df['Sentiment'] = df['Sentiment'].astype(str).astype(float)


        df = df[df['Sentiment'] >= 1 ]
        print("sentiment_analysis - 2")
        print(df)
        return df
    except Exception as e:
        print(f"Error post Sentiment analysis : {e}")

def sentiment_formatter(df):
    
    for index,row in df.iterrows():
        if row['Sentiment'] == 0 :
            df.loc[index, 'Sentiment'] = 'Neutral'
        elif row['Sentiment'] > 0 :
            df.loc[index, 'Sentiment'] = 'Positive'
        else :
            df.loc[index, 'Sentiment'] = 'Negative'

    return df 


# from langchain_community.llms import Ollama
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# def sentiment_analysis_LLAMA(df):
#     print("sentiment_analysis - 1")
    
#     llm = Ollama(model="phi3",callback_manager= CallbackManager([StreamingStdOutCallbackHandler()]))
 
#     df['Sentiment'] = ''


#     for index,row in df.iterrows():
#         df = df[df['Company Name'] != 'BSE']
#         text = row['Summaries']
#         company = row['Company Name']
#         prompt = f"Please analyse these news headlines and give sentiment score between -1 to +1 (ex like  1,0.8, 0.3,-0.5,-0.8,-1 etc) to {company} company based on the stock market news. Sum those sentiment scores to give the net sentiment value of that company . The ouput should only contain the net sentiment value , with no additional commentry , explanation or extra information , like this 'Net Sentiment Score : 1 ' " + " Please process the following headlines: " + text

#         response = llm.invoke(prompt)
#         print(response)

#         df.loc[index, 'Sentiment'] = response


#     df.to_csv(r'C:\Users\ASUS\Projects\UI\StockApp\backend\Predictions\llm_testing\llama_3\phi3.csv')


#     df['Sentiment'] = df['Sentiment'].astype(str).astype(float)


#     df = df[df['Sentiment'] >= 1 ]
#     print("sentiment_analysis - 2")
#     print(df)
#     return df
