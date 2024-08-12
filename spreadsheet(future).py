# This is reference code for future integration of web app (Do Not Grade)

from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API setup
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('{"web":{"client_id":"1091430980943-kjin9tulb374bjammvcmsfan976fi21i.apps.googleusercontent.com","project_id":"orbital-anchor-432019-c0","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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"}} ', scope)
client = 1091430980943-kjin9tulb374bjammvcmsfan976fi21i.apps.googleusercontent.com  

# Replace with your spreadsheet ID and sheet name
spreadsheet_id = 'd/1QxJFwNgL15_-TJRZbrjjyAhQsobeYbtxJt6AHB94UN8/edit?gid=0#gid=0'
sheet_name = 'Buy the Dip Sheet'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        stock_ticker = request.form['stock_ticker']

        # Append data to Google Sheets
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        sheet.append_row([email, stock_ticker])

        return "Data sent to Google Sheets!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials (same as before)
#scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials_file.json',   
 #scope)   

# Authorize and open the spreadsheet using its ID
#client = gspread.authorize(creds)
#spreadsheet_id = '1TQQbfBP7BziHBfw4tYq0acDb87GXkAmFaXp2ExvK_i8' 
#sheet = client.open_by_key(spreadsheet_id).sheet1  # Replace 'sheet1' with the actual sheet name if needed

# Read the values (assuming they're in the first two cells of the first row)
#value1 = sheet.cell(1, 1).value
#value2 = sheet.cell(1, 2).value

#print(value1, value2)

#value1 = sheet.cell(2, 3).value
#value2 = sheet.cell(2, 4).value