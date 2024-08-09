

# Potential input text from subcriber
## NEED to come to this to understand how to log subcribers inputs from the web app 



# ensure pandas is installed 
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv() # look in .env file for env variables

email = input("Please input your email: ") # might need to remove these two lines for web app (but won't run emailchart command without...)
ticker = input("Please input a symbol (e.g. 'NFLX'): ").upper().strip()

AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="demo")

# Fetech stock data from alphavantage API

def fetch_stocks_csv(symbol): 
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={AV_API_KEY}&outputsize=full&datatype=csv"
    return pd.read_csv(request_url) #added pd 


# if __name__ == "__main__": ---> for web app, would need to tab everything below

    #email = input("Please input your email: ")
    #ticker = input("Please input a symbol (e.g. 'NFLX'): ").upper().strip()
    
df = fetch_stocks_csv(ticker)

# Calculate the date five years ago
five_years = datetime.now() - timedelta(days=5*365)
_52_weeks = datetime.now() - timedelta(days=365)

# Convert the date columns to datetime objects
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter the DataFrame
df_five_years = df[df['timestamp'] >= five_years.strftime('%Y-%m-%d')] # note these dataframes only reference the single stock the user inputted
df_52_weeks = df[df['timestamp'] >= _52_weeks.strftime('%Y-%m-%d')]

# TEST CODE 
#print(df_52_weeks.columns)
print(len(df_52_weeks))
df_52_weeks.head()

# Building the parameters: 1) Correction
# a) Define 52-week high, b) define 5-year high; Define "Correction Territory" value for a & b (i.e., a * 90%; b * 90%)

import statistics

high_52_weeks = max(df_52_weeks['high'])
print("52-week high:", high_52_weeks)

high_5_years = max(df_five_years['high'])
print("5-year high:", high_5_years) # not accounting for stock splits... maybe use polygon

# Setting variables for correction territory values

correction_52_week = round(high_52_weeks * 0.9,2)
print("52-week correction territory:", correction_52_week)
_20_drop_52_week = round(high_52_weeks * 0.8,2)
_30_drop_52_week = round(high_52_weeks * 0.7,2)
_40_drop_52_week = round(high_52_weeks * 0.6,2)

# DO WE NEED THIS CORRECTIONS ON THE FIVE YEARS OF DATA??

correction_5_year = round(high_5_years * 0.9,2)
print("5-year correction territory:", correction_5_year)
_20_drop_5_year = round(high_5_years * 0.8,2)
_30_drop_5_year = round(high_5_years * 0.7,2)
_40_drop_5_year = round(high_5_years * 0.6,2)

# Comparing todays closing price vs 52 week high

if df_52_weeks['adjusted_close'][0] < correction_52_week and df_52_weeks['adjusted_close'][1] > correction_52_week:
    signal = True
elif df_52_weeks['adjusted_close'][0] < _20_drop_52_week and df_52_weeks['adjusted_close'][1] > _20_drop_52_week:
    signal = True
elif df_52_weeks['adjusted_close'][0] < _30_drop_52_week and df_52_weeks['adjusted_close'][1] > _30_drop_52_week:
    signal = True
elif df_52_weeks['adjusted_close'][0] < _40_drop_52_week and df_52_weeks['adjusted_close'][1] > _40_drop_52_week:
    signal = True
else :
    signal = False 
    
# 5 year comparison 
if df_52_weeks['adjusted_close'][0] < correction_5_year and df_52_weeks['adjusted_close'][1] > correction_5_year:
    signal_ = True
elif df_52_weeks['adjusted_close'][0] < _20_drop_5_year and df_52_weeks['adjusted_close'][1] > _20_drop_5_year:
    signal_ = True
elif df_52_weeks['adjusted_close'][0] < _30_drop_5_year and df_52_weeks['adjusted_close'][1] > _30_drop_5_year:
    signal_ = True
elif df_52_weeks['adjusted_close'][0] < _40_drop_5_year and df_52_weeks['adjusted_close'][1] > _40_drop_5_year:
    signal_ = True
else :
    signal_ = False 

# THIS SECTION IS TO CALCULATE AND COMPARE 50-DAY VS 200-DAY MOVING AVERAGES
### COMMENTED THIS SECTION OUT FOR NOW 8/7/24
# Ensure the data is sorted by date
#df_52_weeks = df_52_weeks.sort_index(ascending=False)

# Calculate 50-day and 200-day MA

#df_52_weeks['MA50'] = df_52_weeks['adjusted_close'].rolling(window=50).mean()
#df_52_weeks['MA200'] = df_52_weeks['adjusted_close'].rolling(window=200).mean()

# Get today's and yesterday's 50-day and 200-day MA values

#today_ma50 = df_52_weeks['MA50'].iloc[-1]
#yesterday_ma50 = df_52_weeks['MA50'].iloc[-2]
#today_ma200 = df_52_weeks['MA200'].iloc[-1]
#yesterday_ma200 = df_52_weeks['MA200'].iloc[-2]
#today = df_52_weeks['timestamp'].iloc[-1]
#today_close = df_52_weeks['adjusted_close'].iloc[-1]

# Check for crossover (above or below)

#if (today_ma50 > today_ma200 and yesterday_ma50 < yesterday_ma200):
    # Signal = 1 --> "signal" to help with knowing if we need to send an email notification
    #print("50-day MA crossed above 200-day MA today.")
#elif (today_ma50 < today_ma200 and yesterday_ma50 > yesterday_ma200):
    #print("50-day MA crossed below 200-day MA today.")
    # Signal = -1
#else:
    #if today_ma50 > today_ma200:
        #print("No crossover today, and the 50-day Moving Average is above the 200-day Moving Average.")
    #else:
        #print("No crossover today, and the 50-day Moving Average is below the 200-day Moving Average.")

#print(f"Closing Price as of",today.strftime('%Y-%m-%d'),round(today_close,2))
#print("50-day Moving Average:", round(today_ma50,2))
#print("200-day Moving Average:", round(today_ma200,2))


