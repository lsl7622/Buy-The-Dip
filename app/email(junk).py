# This code is for sending email with metadata and chart

# Ths pulls the emails we put into the txt file, which I'm sure we could automate so that it adds user submissions via the web app with more digging
# This interprets and reads the subscriber preferences
def get_subscribers(file_path='subscribers.txt'):
    subscribers = []
    with open(file_path, 'r') as file:
        for line in file:
            email, ticker = line.strip().split(',')
            subscribers.append({
                'email': email, #med9789@stern.nyu.edu
                'ticker': ticker, #APPL
            })
    return subscribers


# This is where we out our four final functions discussed to generate email contents

def create_email_content(ticker, drop_percentage): #prepares the data content that will be uniform across all emails.
    subject = f'Alert: {ticker} dropped by {drop_percentage:.2f}%'
    body = f'The stock {ticker} has dropped by {drop_percentage:.2f}% in the last day.'
    return subject, body

def send_email(to_email, subject, body): #send email function
    from_email = os.getenv('chrislucasmason@gmail.com')
    from_password = os.getenv('chrislucasmason12345')

    msg = MIMEText(body) #this is where we set the content
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.example.com', 587) as server: #this is how the email is sent via network.
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        
def send_stock_alerts(): #This is the magic send.function that will send emails based on stock performance or whatever conditional equation we'd prefer.
    subscribers = get_subscribers()

    for subscriber in subscribers:
        email = subscriber['email']
        ticker = subscriber['ticker']
        if signal == 1:
            subject, body = create_email_content(ticker, drop_percentage)
            send_email(email, subject, body)
        elif signal_ == 1:
            subject, body = create_email_content(ticker, drop_percentage)
            send_email(email, subject, body)
        else:
            
            
if __name__ == '__main__': #ensures that certain code is only executed when the script is run directly
    send_stock_alerts()
    
    
if signal == 1:
    # Prepare email content
    body_functions = [
        lambda: get_stock_info('AAPL'),   # Example functions
        get_signal_analysis               # You'll likely have more
    ]
    subject = "Stock Signal Alert!"

    # Send email (if signal == 1)
    send_signal_email(signal, subscribers, subject, body_functions)