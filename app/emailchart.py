import smtplib
import os
from email.mime.text import MIMEText
from data import ticker, email
from meta_data import fig
from dotenv import load_dotenv
load_dotenv()

def send_email_with_chart(to_email, body, fig): #send email function
    from_email = os.getenv('YOUR_EMAIL_ADDRESS')
    from_password = os.getenv('YOUR_EMAIL_PASSWORD')

    msg = MIMEText(body) #this is where we set the content
    msg['Subject'] = f'Stock Alert: {ticker}'
    msg['From'] = from_email
    msg['To'] = to_email

    # Add text to the email body

    body = f"Here's the candlestick chart for {ticker}:\n\n" 
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)

    # Save the Plotly chart as an image
    fig.write_image("chart.png")

    # Attach the chart image to the email
    with open('chart.png', 'rb') as img_file:
        img_part = MIMEImage(img_file.read())
        img_part.add_header('Content-Disposition', 'attachment', filename='chart.png')
        msg.attach(img_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server: #this is how the email is sent via network.
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
    
    print(f"Email with chart sent to {to_email}")

# Sending the email:
send_email_with_chart(email, ticker, fig) # need to define the body?