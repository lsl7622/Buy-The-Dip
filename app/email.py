# This code is for sending email with metadata and chart

# Ths pulls the emails we put into the txt file, which I'm sure we could automate so that it adds user submissions via the web app with more digging
# This interprets and reads the subscriber preferences
def get_subscribers(file_path='subscribers.txt'):
    subscribers = []
    with open(file_path, 'r') as file:
        for line in file:
            email, ticker, threshold = line.strip().split(',')
            subscribers.append({
                'email': email, #med9789@stern.nyu.edu
                'ticker': ticker, #APPL
                'threshold': float(threshold) #10
            })
    return subscribers

