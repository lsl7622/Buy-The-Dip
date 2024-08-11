import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()
import statistics
import finnhub
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import   
MIMEImage
import io
import plotly.io as pio

# ... (rest of your existing code)

def five_yr_candle_stick_chart(df_five_years, ticker):
    # ... (your existing chart generation code)
    return fig 

def ticker_meta_data(ticker):
    # ... (your existing metadata retrieval code)

def get_subscribers(file_path='subscribers.txt'):
    # ... (your existing subscriber retrieval code)

def create_email_content(ticker, drop_percentage, fig, metadata):
    subject = f'Alert: {ticker} dropped by {drop_percentage:.2f}%'
    body = f'The stock {ticker} has dropped by {drop_percentage:.2f}% in the last day.\n\n'
    body += metadata + '\n\n'  # Add metadata to the email body
    return subject, body

def send_email(to_email, subject, body, fig):
    from_email = os.getenv('EMAIL_ADDRESS')
    from_password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Attach the chart image
    img_bytes = pio.to_image(fig, format='png')
    img = MIMEImage(img_bytes)
    img.add_header('Content-ID', '<chart>')  # Set a Content-ID for referencing in the HTML
    msg.attach(img)

    # Create the HTML body with the embedded chart
    body_html = f"""
    <html>
    <body>
    {body}<br>
    <img src="cid:chart">
    </body>
    </html>
    """
    msg.attach(MIMEText(body_html, 'html'))

    with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server details
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)

def send_stock_alerts():
    subscribers = get_subscribers()

    for subscriber in subscribers:
        email = subscriber['email']
        ticker = subscriber['ticker']

        # Fetch data and generate chart only if a signal is triggered
        if signal == 1 or signal_ == 1:
            df = fetch_stocks_csv(ticker)
            df_five_years = df[df['timestamp'] >= five_years.strftime('%Y-%m-%d')]
            df_52_weeks = df[df['timestamp'] >= _52_weeks.strftime('%Y-%m-%d')]

            # ... (rest of your signal calculation logic)

            if signal == 1 or signal_ == 1:
                fig = five_yr_candle_stick_chart(df_five_years, ticker)
                metadata = ticker_meta_data(ticker)  # Get metadata as a string

                # Calculate drop_percentage based on your logic
                drop_percentage = ... 

                subject, body = create_email_content(ticker, drop_percentage, fig, metadata)
                send_email(email, subject, body, fig)

if __name__ == '__main__':
    send_stock_alerts()