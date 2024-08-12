import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv() # look in .env file for env variables

credentials_file = os.getenv("Client_ID")"

# Define the scope and credentials (same as before)
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Credentials
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(creds)

# Authorize and open the spreadsheet using its ID
spreadsheet_id = '1TQQbfBP7BziHBfw4tYq0acDb87GXkAmFaXp2ExvK_i8' 
sheet = client.open_by_key(spreadsheet_id).sheet1  # Replace 'sheet1' with the actual sheet name if needed

# Get all data from the sheet
data = sheet.get_all_records()

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('data.csv', index=False)

print("Data has been extracted from Google Sheet and saved as data.csv")

# Save DataFrame to CSV
# df.to_csv('data.csv', index=False)