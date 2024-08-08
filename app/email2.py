to_email = 'christopher.frye94@gmail.com'

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

def send_email(to_email, subject, body): #send email function
    from_email = os.getenv('chrislucasmason@gmail.com')
    from_password = os.getenv('chrislucasmason12345')

    msg = MIMEText(body) #this is where we set the content
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

send_email