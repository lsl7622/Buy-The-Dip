
# this is the "web_app/routes/buythedip.py" file ...

from flask import Flask, Blueprint, request, render_template, redirect, flash
import plotly.io as pio
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta
import os

AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="demo")

# from app.data_webapp import fetch_stocks_csv
#from app.data import df_five_years
from app.meta_data import ticker_meta_data
from app.candlestick_MA_chart import five_yr_candle_stick_chart
from app.emailchart import send_email_with_chart

app = Flask(__name__)

buythedip_routes = Blueprint("buythedip_routes", __name__)

@buythedip_routes.route("/") # this route will display the form
def index():
    print("HOME...") # this is showing up in terminal/server log when someone visits this route
    return render_template("home.html")

@buythedip_routes.route("/dashboard", methods=["POST"]) # this route will fetch data based on the form route and pass to display page
def dashboard():
    print("DASHBOARD...") # this is showing up in terminal/server log when someone visits this route
    request_data = dict(request.form)
    symbol = request_data.get("symbol")
    email = request_data.get("email")
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5 = ticker_meta_data(symbol)

    # Get five years of data

    def fetch_stocks_csv(symbol): 
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={AV_API_KEY}&outputsize=full&datatype=csv"
        return pd.read_csv(request_url)
    
    df = fetch_stocks_csv(symbol)

    # Calculate the date five years ago
    five_years = datetime.now() - timedelta(days=5*365)

    # Convert the date columns to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filter the DataFrame
    df_five_years = df[df['timestamp'] >= five_years.strftime('%Y-%m-%d')]

    # Formatting Meta Data
    formatted_current_price=f"{current_price:.2f}"
    formatted_meta_data1=f"${meta_data1:.2f}"
    formatted_meta_data2=f"${meta_data2:.2f}"
    formatted_meta_data5=f"{meta_data5: .2f}"

    # Get candlestick chart Figure
    fig = five_yr_candle_stick_chart(df_five_years, symbol)

    # Convert figure to HTML

    chart_html = pio.to_html(fig, full_html=False)

    # Send thank you email with chart
    send_email_with_chart(email, symbol, df_five_years)

    return render_template("dashboard.html", 
                           symbol=symbol,
                           current_price=formatted_current_price,
                           meta_data1=formatted_meta_data1,
                           meta_data2=formatted_meta_data2,
                           meta_data3=meta_data3,
                           meta_data5=formatted_meta_data5,
                           chart_html=chart_html
                           )