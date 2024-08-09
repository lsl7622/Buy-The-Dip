# need to pip install -U kaleido (for image chart)

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.data import ticker, email, df_five_years
from app.meta_data import five_yr_candle_stick_chart, ticker_meta_data
import finnhub 
ticker_meta_data(ticker)
fig1 = five_yr_candle_stick_chart(df_five_years, ticker)

from dotenv import load_dotenv
load_dotenv()

F_API_KEY = os.getenv("FINNHUB_API_KEY")
# Setup client
finnhub_client = finnhub.Client(api_key= F_API_KEY) #cqnqotpr01qo8864pu70cqnqotpr01qo8864pu7g (CF added to notebook secrets)


def ticker_meta_data(ticker):
  finance_data = []
  current_price = finnhub_client.quote(ticker)
  current_price = current_price['c']
  print('Current Price','$',current_price)
  finance_data.append(finnhub_client.company_basic_financials(f'{ticker}', 'all'))
  meta_data1 = finance_data[0]['metric']['52WeekHigh']
  meta_data2 = finance_data[0]['metric']['52WeekLow']
  meta_data3 = finance_data[0]['metric']['52WeekLowDate']
  meta_data4 = ((meta_data1 - meta_data2)/(meta_data1))*100
  meta_data5 = finance_data[0]['metric']['beta']
  # Include Yahoo Finance URL
  print('See more on Yahoo Finance:',f"https://finance.yahoo.com/quote/{ticker}/") # ticker is the varibale used above
  return current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5
# Example usage:
#ticker_meta_data(f'{ticker}')


def send_email_with_chart(to_email, body, fig1): #send email function
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEMultipart() #this is where we set the content
    msg['Subject'] = f'Stock Alert: {ticker} & Candlestick Chart'
    msg['From'] = from_email
    msg['To'] = to_email

    # Add text to the email body
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5 = ticker_meta_data(ticker)

    body = f"""
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

    with smtplib.SMTP('smtp.gmail.com', 587) as server: #this is how the email is sent via network.
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
    
    print(f"Email with chart sent to {to_email}")

# Sending the intial email:
send_email_with_chart(email, ticker, fig1) # need to define the body?

# Sending the conditional email: 
#if signal == 1:
    #send_email_with_chart(email, ticker, fig1)
#elif signal_ == 1:
    #send_email_with_chart(email, ticker, fig1)
#else:
    #None 