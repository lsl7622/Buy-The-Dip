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