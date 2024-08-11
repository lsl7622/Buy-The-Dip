import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os 
from app.meta_data import ticker_meta_data

load_dotenv()

# Load the CSV file
file_path = 'Local_Python_Project_Sheet - Sheet1.csv'
df = pd.read_csv(file_path)

# Email credentials
smtp_server = 'your_smtp_server'  # e.g., 'smtp.gmail.com'
smtp_port = 587  # or 465 for SSL
email_address = os.getenv('YOUR_EMAIL_ADDRESS')
email_password = os.getenv('YOUR_EMAIL_PASSWORD')

def send_email(to_email, ticker): #send email function
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEText(body) #this is where we set the content
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    #get metadata
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5 = ticker_meta_data(ticker)

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
    Beta: {meta_data5:.2f}
    See more on Yahoo Finance: https://finance.yahoo.com/quote/{ticker}/
    """

    with smtplib.SMTP('smtp.gmail.com', 587) as server: #this is how the email is sent via network.
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        
    print(f'Email sent to {to_email}')


# Read the CSV file and send emails
for index, row in df.iterrows():
    send_email(row['email'], row['ticker'])
