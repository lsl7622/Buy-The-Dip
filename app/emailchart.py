# need to pip install -U kaleido (for image chart)

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.data import ticker, email, df_five_years
from app.meta_data import five_yr_candle_stick_chart, ticker_meta_data
ticker_meta_data(ticker)
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