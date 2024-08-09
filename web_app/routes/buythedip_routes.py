
# this is the "web_app/routes/buythedip.py" file ...

from flask import Blueprint, request, render_template, redirect, flash

# from app.data import fetch_stocks_csv
from app.meta_data import ticker_meta_data

buythedip_routes = Blueprint("buythedip_routes", __name__)

@buythedip_routes.route("/") # this route will display the form
def index():
    print("HOME...") # this is showing up in terminal/server log when someone visits this route
    # return "Welcome Home" # this is showing up in Web App when someone visits this route
    return render_template("home.html")

@buythedip_routes.route("/dashboard", methods=["POST"]) # this route will fetch data based on the form route and pass to display page
def dashboard():
    print("DASHBOARD...") # this is showing up in terminal/server log when someone visits this route
    # return "Welcome Home" # this is showing up in Web App when someone visits this route
    request_data = dict(request.form)
    symbol = request_data.get("symbol")
    email = request_data.get("email")
    current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5 = ticker_meta_data(symbol)

    return render_template("dashboard.html", 
                           symbol = symbol,
                           current_price = current_price
                           )