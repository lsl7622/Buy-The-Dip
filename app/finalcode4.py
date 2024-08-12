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

# Function to fetch stock data
def fetch_stocks_csv(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={AV_API_KEY}&outputsize=full&datatype=csv"
    return pd.read_csv(request_url)

# Function to send an email with the chart
def send_email_with_chart(to_email, ticker, df_five_years, signal):
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['Subject'] = f'Stock Alert: {ticker} & Candlestick Chart'
    msg['From'] = from_email
    msg['To'] = to_email

    # Generate the chart
    fig1 = five_yr_candle_stick_chart(df_five_years, ticker)

    # Get meta data
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, = ticker_meta_data(ticker)

    if signal:
        body = f"""
        Thank you for signing up to receive alerts for {ticker}

        Current Price: ${current_price:.2f}
        52-week high: ${meta_data1:.2f}
        5-year high: ${meta_data1:.2f}
        52-week correction territory: ${meta_data2 * 0.9:.2f}
        5-year correction territory: ${meta_data2 * 0.9:.2f}
        52 Week High: ${meta_data1:.2f}
        52 Week Low & Date: ${meta_data2:.2f} , {meta_data3}
        52 Week Percent change: {meta_data4:.2f} %
        See more on Yahoo Finance: https://finance.yahoo.com/quote/{ticker}/
        """
    else:
        body = f"""
        Thank you for signing up to receive alerts for {ticker}

        There is no sign of a correction from its 52-week high today.
        
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
    
    

# Function to check if the stock is in correction territory
def check_correction(df_52_weeks):
    high_52_weeks = df_52_weeks['high'].max()
    correction_52_week = high_52_weeks * 0.9

    recent_close = df_52_weeks['adjusted_close'].iloc[-1]

    if recent_close < correction_52_week:
        return True
    return False

# Load the CSV file with tickers and emails
file_path = 'Local_Python_Project_Sheet - Sheet1.csv'
df_contacts = pd.read_csv(file_path)

# Loop through each ticker and email pair
for index, row in df_contacts.iterrows():
    ticker = row['Ticker']
    email = row['Email']

    df = fetch_stocks_csv(ticker)

    # Calculate the date five years ago
    five_years = datetime.now() - timedelta(days=5*365)
    _52_weeks = datetime.now() - timedelta(days=365)

    # Convert the date columns to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filter the DataFrame
    df_five_years = df[df['timestamp'] >= five_years.strftime('%Y-%m-%d')]
    df_52_weeks = df[df['timestamp'] >= _52_weeks.strftime('%Y-%m-%d')]

    # Check if the stock is in correction territory
    signal = check_correction(df_52_weeks)

    # Send the appropriate email
    send_email_with_chart(email, ticker, df_five_years, signal)
