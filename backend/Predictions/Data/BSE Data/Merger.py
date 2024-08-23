#The data is collected from https://www.bseindia.com/corporates/List_Scrips.html
import pandas as pd
df_1 = pd.read_csv('/home/rahul-/Projects/Stock/Data/BSE Data/Equity T+0 Active.csv')
df_2 = pd.read_csv('/home/rahul-/Projects/Stock/Data/BSE Data/Equity T+1 Active.csv')
print(df_1)
print("********************************************************")
print(df_2)
print("********************************************************")

df = pd.concat([df_1,df_2],axis=0)
df = df.reset_index(drop=True)
print("********************************************************")
df.drop_duplicates(inplace=True)
print(df)
df.to_csv('/home/rahul-/Projects/Stock/Data/BSE Data/BSE_total.csv')
