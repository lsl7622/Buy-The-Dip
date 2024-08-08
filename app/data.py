

# Potential input text from subcriber
## NEED to come to this to understand how to log subcribers inputs from the web app 
email = input("Please input your email: ")
ticker = input("Please input a symbol (e.g. 'NFLX'): ").upper().strip()

# Fetech stock data from alphavantage API

def fetch_stocks_csv(symbol = ticker): 
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={AV_API_KEY}&outputsize=full&datatype=csv"
    return read_csv(request_url)

df = fetch_stocks_csv()

# Calculate the date five years ago
five_years = datetime.now() - timedelta(days=5*365)
_52_weeks = datetime.now() - timedelta(days=365)

# Convert the date columns to datetime objects
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter the DataFrame
df_five_years = df[df['timestamp'] >= five_years.strftime('%Y-%m-%d')] # note these dataframes only reference the single stock the user inputted
df_52_weeks = df[df['timestamp'] >= _52_weeks.strftime('%Y-%m-%d')]

print(df_52_weeks.columns)
print(len(df_52_weeks))
df_52_weeks.head()

