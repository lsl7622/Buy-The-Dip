import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from app.meta_data import ticker_meta_data
import finnhub 

load_dotenv()

# Load the CSV file
file_path = 'Local_Python_Project_Sheet - Sheet1.csv'
df = pd.read_csv(file_path)

F_API_KEY = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key= F_API_KEY)

def ticker_meta_data(ticker):
  finance_data = []
  current_price = finnhub_client.quote(ticker)
  current_price = current_price['c']
  print('Current Price','$',current_price)
  finance_data.append(finnhub_client.company_basic_financials(f'{ticker}', 'all'))

  metrics = finance_data[0]['metric']
  meta_data1 = metrics.get('52WeekHigh', 0)
  meta_data2 = metrics.get('52WeekLow', 0)
  meta_data3 = metrics.get('52WeekLowDate', 'N/A')
  meta_data4 = ((meta_data1 - meta_data2) / meta_data1) * 100 if meta_data1 != 0 else 0
  meta_data5 = metrics.get('beta', 'N/A')
  # Include Yahoo Finance URL
  print('See more on Yahoo Finance:',f"https://finance.yahoo.com/quote/{ticker}/") # ticker is the varibale used above
  return current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5

# Email credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
email_address = os.getenv('YOUR_EMAIL_ADDRESS')
email_password = os.getenv('YOUR_EMAIL_PASSWORD')

def send_email(to_email, ticker):
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    # Get metadata
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5 = ticker_meta_data(ticker)

    # Email subject and body
    subject = f'Alert for {ticker}'
    body = f"""
    Thank you for signing up to receive alerts for {ticker}

    Current Price: ${current_price:.2f}
    52-week high: ${meta_data1:.2f}
    5-year high: ${meta_data1:.2f}
    52-week correction territory: ${meta_data2 * 0.9:.2f}
    5-year correction territory: ${meta_data2 * 0.9:.2f}
    52 Week High: $ {meta_data1:.2f}
    52 Week Low & Date: $ {meta_data2:.2f} , {meta_data3}
    52 Week Percent change: {meta_data4:.2f} %
    Beta: {meta_data5 if isinstance(meta_data5, (int, float)) else meta_data5}
    See more on Yahoo Finance: https://finance.yahoo.com/quote/{ticker}/
    """

    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)

    print(f'Email sent to {to_email}')

# Read the CSV file and send emails
for index, row in df.iterrows():
    send_email(row['Email'], row['Ticker'])