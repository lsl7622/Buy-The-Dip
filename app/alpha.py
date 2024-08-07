# this is the "app/alpha.py" file....

import os
from dotenv import load_dotenv

load_dotenv() # look in .env file for env variables

AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

F_API_KEY = os.getenv("FINNHUB_API_KEY")