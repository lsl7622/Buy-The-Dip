# This is our final version of code that runs conditional statements from a user subscribe list that is converted into a CSV and email are sent to the subcribers! 

import pandas as pd
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import plotly.io as pio
from dotenv import load_dotenv
from app.candlestick_MA_chart import five_yr_candle_stick_chart
from app.meta_data import ticker_meta_data
import finnhub
from datetime import datetime, timedelta

load_dotenv()

# Setup Finnhub client
F_API_KEY = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=F_API_KEY)
AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="demo")

# meta_data fucntion
def ticker_meta_data(ticker):
    finance_data = []
    current_price = finnhub_client.quote(ticker)
    current_price = current_price['c']
    print('Current Price', '$', current_price)
    finance_data.append(finnhub_client.company_basic_financials(f'{ticker}', 'all'))

    metrics = finance_data[0]['metric']
    meta_data1 = metrics.get('52WeekHigh', 0)
    meta_data2 = metrics.get('52WeekLow', 0)
    meta_data3 = metrics.get('52WeekLowDate', 'N/A')
    meta_data4 = ((meta_data1 - meta_data2) / meta_data1) * 100 if meta_data1 != 0 else 0
    meta_data5 = metrics.get('beta', 'N/A')
    
    print('See more on Yahoo Finance:', f"https://finance.yahoo.com/quote/{ticker}/")
    return current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5


# send email functions including True and False emails
def send_email_with_chart_True(to_email, ticker, df_five_years):
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['Subject'] = f'Stock Alert: {ticker} & Candlestick Chart'
    msg['From'] = from_email
    msg['To'] = to_email
    
    # Generate the chart
    fig1 = five_yr_candle_stick_chart(df_five_years, ticker)

    # Get meta data
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5 = ticker_meta_data(ticker)

    body = f"""
    Thank you for signing up to receive alerts for {ticker}
    
    Alert! This stock has entered correction territory! 

    Current Stock Price: ${current_price:.2f}
    52-week high: ${meta_data1:.2f}
    5-year high: ${meta_data1:.2f}
    52-week correction territory: ${meta_data2 * 0.9:.2f}
    5-year correction territory: ${meta_data2 * 0.9:.2f}
    52 Week High: ${meta_data1:.2f}
    52 Week Low & Date: ${meta_data2:.2f} , {meta_data3}
    52 Week Percent change: {meta_data4:.2f} %
    Beta: {meta_data5 if isinstance(meta_data5, (int, float)) else meta_data5}
    See more on Yahoo Finance: https://finance.yahoo.com/quote/{ticker}/
    """
    
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)

    # Save the Plotly chart as an image
    fig1.write_image("chart.png")

    # Attach the chart image to the email
    with open("chart.png", 'rb') as f:
        img_part = MIMEImage(f.read())
        img_part.add_header('Content-Disposition', 'attachment', filename='chart.png')
        msg.attach(img_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
    
    print(f"Email with chart sent to {to_email}")


def send_email_with_chart_False(to_email, ticker, df_five_years):
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['Subject'] = f'Stock Alert: {ticker} & Candlestick Chart'
    msg['From'] = from_email
    msg['To'] = to_email
    
    # Generate the chart
    fig1 = five_yr_candle_stick_chart(df_five_years, ticker)

    # Get meta data
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5 = ticker_meta_data(ticker)

    body = f"""
    Thank you for signing up to receive alerts for {ticker}.
    
    There is no sign of a correction for this stock.
    
    Current Stock Price: ${current_price:.2f}
    52-week high: ${meta_data1:.2f}
    5-year high: ${meta_data1:.2f}
    52-week correction territory: ${meta_data2 * 0.9:.2f}
    5-year correction territory: ${meta_data2 * 0.9:.2f}
    52 Week High: ${meta_data1:.2f}
    52 Week Low & Date: ${meta_data2:.2f} , {meta_data3}
    52 Week Percent change: {meta_data4:.2f} %
    Beta: {meta_data5 if isinstance(meta_data5, (int, float)) else meta_data5}
    See more on Yahoo Finance: https://finance.yahoo.com/quote/{ticker}/
    """
    
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)

    # Save the Plotly chart as an image
    fig1.write_image("chart.png")

    # Attach the chart image to the email
    with open("chart.png", 'rb') as f:
        img_part = MIMEImage(f.read())
        img_part.add_header('Content-Disposition', 'attachment', filename='chart.png')
        msg.attach(img_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
    
    print(f"Email with chart sent to {to_email}")



# Define fetch_stocks_csv once 
def fetch_stocks_csv(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={AV_API_KEY}&outputsize=full&datatype=csv"
    return pd.read_csv(request_url)

# Load the CSV file
file_path = 'Local_Python_Project_Sheet - Sheet1.csv'
df = pd.read_csv(file_path)

# Verify columns
print(df.columns)

# Read the CSV file and send email
for index, row in df.iterrows():
    ticker = row['Ticker']  
    email = row['Email']    

    try:
        df_stock = fetch_stocks_csv(ticker)

        # Calculate the date five years ago
        five_years_ago = datetime.now() - timedelta(days=5*365)
        _52_weeks_ago = datetime.now() - timedelta(days=365)

        # Convert the date columns to datetime objects
        df_stock['timestamp'] = pd.to_datetime(df_stock['timestamp'])

        # Filter the DataFrame
        df_five_years = df_stock[df_stock['timestamp'] >= five_years_ago]
        df_52_weeks = df_stock[df_stock['timestamp'] >= _52_weeks_ago]

        # Calculate the signal 
        high_52_weeks = df_52_weeks['high'].max()
        correction_52_week = high_52_weeks * 0.9
        current_price = df_52_weeks['adjusted_close'][0]  # first row is the latest data
        signal = current_price < correction_52_week

        if signal:
            send_email_with_chart_True(email, ticker, df_five_years)
        else:
            send_email_with_chart_False(email, ticker, df_five_years)

    except Exception as e:
        print(f"Error processing {ticker} for {email}: {e}")