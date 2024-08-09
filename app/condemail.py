# NOW WANT TO ADD CONDITIONS

# THIS FIRST CODE IS VERY BASIC EMAIL SENDING

import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

def get_subscribers(file_path='subscribers.txt'):
    subscribers = []
    with open(file_path, 'r') as file: #where is r defined?
        for line in file:
            email, ticker = line.strip().split(',')
            subscribers.append({
                'email': email, #med9789@stern.nyu.edu
                'ticker': ticker, #APPL
            })
    return subscribers

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2d")
    if len(hist) < 2:
        return None, None
    latest_close = hist['Close'][-1]
    previous_close = hist['Close'][-2]
    return latest_close, previous_close

# This is where we out our four final functions discussed to generate email contents
def create_email_content(ticker, drop_percentage): #prepares the data content that will be uniform across all emails.
    subject = f'Alert: {ticker} dropped by {drop_percentage:.2f}% today'
    body = f'''The stock {ticker} has dropped by {drop_percentage:.2f}% in the last day.

    Stock Analysis for {ticker}

    Current Price: ${current_price:.2f}  # Format with 2 decimal places
    52-week high: ${meta_data1:.2f}
    5-year high: ${meta_data1:.2f}  # Assuming this is the same as 52-week high
    52-week correction territory: ${meta_data2 * 0.9:.2f}  # 10% below 52-week low
    5-year correction territory: ${meta_data2 * 0.9:.2f}   # Assuming same as 52-week
    52 Week High: $ {meta_data1:.2f}
    52 Week Low & Date: $ {meta_data2:.2f} , {meta_data3}
    52 Week Percent change: {meta_data4:.2f} %
    Beta: {meta_data5:.2f}
    See more on Yahoo Finance: https://finance.yahoo.com/quote/{ticker}/
    '''
    return subject, body

def send_email(to_email, subject, body): #send email function
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEText(body) #this is where we set the content
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server: #this is how the email is sent via network.
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)

def send_stock_alerts(): #This is the magic send.function that will send emails based on stock performance or whatever conditional equation we'd prefer.
    subscribers = get_subscribers()

    for subscriber in subscribers:
        email = subscriber['email']
        ticker = subscriber['ticker']

        latest_close, previous_close = get_stock_price(ticker)
        if latest_close is None or previous_close is None:
            continue

        drop_percentage = ((previous_close - latest_close) / previous_close) * 100
        if signal == True: 
            subject, body = create_email_content(ticker, drop_percentage)
            send_email(email, subject, body)

if __name__ == '__main__': #ensures that certain code is only executed when the script is run directly
    send_stock_alerts()

# Sending the email:
send_email('christopher.frye94@gmail.com', 'Test Email', 'This is a test email.')


## THIS SET OF CODE IS SENDING CANDLESTICK CHART VIA EMAIL

# need to pip install -U kaleido (for image chart)

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.data import ticker, email, df_five_years
from app.meta_data import five_yr_candle_stick_chart, ticker_meta_data
fig1 = five_yr_candle_stick_chart(df_five_years, ticker)

from dotenv import load_dotenv
load_dotenv()

def send_email_with_chart(to_email, body, fig1): #send email function
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEMultipart() #this is where we set the content
    msg['Subject'] = f'Stock Alert: {ticker} & Candlestick Chart'
    msg['From'] = from_email
    msg['To'] = to_email

    # Add text to the email body

    body = f"""Here's the candlestick chart for {ticker}:\n\n
    Current Price: ${current_price}
    
    """ # this is where the text in the body of the email appears
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)

    # Save the Plotly chart as an image
    fig1.write_image("chart.png")

    # Attach the chart image to the email
    with open("chart.png", 'rb') as f:
        img_part = MIMEImage(f.read())
        img_part.add_header('Content-Disposition', 'attachment', filename='chart.png')
        msg.attach(img_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server: #this is how the email is sent via network.
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
    
    print(f"Email with chart sent to {to_email}")

# Sending the email:
send_email_with_chart(email, ticker, fig1) # need to define the body?