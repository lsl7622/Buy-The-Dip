import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials (same as before)
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials_file.json',   
 scope)   

# Authorize and open the spreadsheet using its ID
client = gspread.authorize(creds)
spreadsheet_id = '1TQQbfBP7BziHBfw4tYq0acDb87GXkAmFaXp2ExvK_i8' 
sheet = client.open_by_key(spreadsheet_id).sheet1  # Replace 'sheet1' with the actual sheet name if needed

# Read the values (assuming they're in the first two cells of the first row)
value1 = sheet.cell(1, 1).value
value2 = sheet.cell(1, 2).value

print(value1, value2)

value1 = sheet.cell(2, 3).value
value2 = sheet.cell(2, 4).value

value3=365
#Test
