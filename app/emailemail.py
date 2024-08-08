import smtplib
import os
from email.mime.text import MIMEText

def send_email(to_email, subject, body): #send email function
    from_email = os.getenv('chrislucasmason@gmail.com')
    from_password = os.getenv('chrislucasmason12345')

    msg = MIMEText(body) #this is where we set the content
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server: #this is how the email is sent via network.
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)

# Example usage:
send_email('christopher.frye94@gmail.com', 'Test Email', 'This is a test email.')