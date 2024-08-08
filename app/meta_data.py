import pandas as pd
import plotly.graph_objects as go
import os

def five_yr_candle_stick_chart(df_five_years, ticker):
    """
    Generates a 5-year candlestick chart for a given ticker symbol.

    Args:
        df_five_years: A pandas DataFrame containing the 5-year historical data
                       with columns 'timestamp', 'open', 'high', 'low', and 'close'.
        ticker: The ticker symbol of the stock.

    Returns:
        A Plotly Figure object representing the candlestick chart.
    """

    # Create a copy of df_filtered and rename columns
    df1 = df_five_years[['timestamp', 'open', 'high', 'low', 'close']].copy()
    df1.columns = ['Date', 'Open', 'High', 'Low', 'Close']

    # Convert Date column to datetime
    df1['Date'] = pd.to_datetime(df1['Date'])

    # Create the candlestick figure
    fig = go.Figure(data=[go.Candlestick(
        x=df1['Date'],
        open=df1['Open'],
        high=df1['High'],
        low=df1['Low'],
        close=df1['Close']
    )])

    # Customize the chart appearance
    fig.update_layout(
        title=f'5 Year Chart of {ticker}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    # Additional customizations (optional)
    fig.update_xaxes(
        tickangle=-45,
        tickformat="%Y-%m-%d"
    )

    # Show the plot
    #fig.show()
    return fig  # Return the figure object

# Example usage:
#five_yr_candle_stick_chart(df_five_years, ticker)

## importing metadata

import finnhub

F_API_KEY = os.getenv("FINNHUB_API_KEY")
# Setup client
finnhub_client = finnhub.Client(api_key= F_API_KEY) #cqnqotpr01qo8864pu70cqnqotpr01qo8864pu7g (CF added to notebook secrets)

def ticker_meta_data(ticker):
  finance_data = []
  current_price = finnhub_client.quote(ticker)
  current_price = current_price['c']
  print('Current Price','$',current_price)
  finance_data.append(finnhub_client.company_basic_financials(f'{ticker}', 'all'))
  meta_data1 = finance_data[0]['metric']['52WeekHigh']
  meta_data2 = finance_data[0]['metric']['52WeekLow']
  meta_data3 = finance_data[0]['metric']['52WeekLowDate']
  meta_data4 = ((meta_data1 - meta_data2)/(meta_data1))*100
  meta_data5 = finance_data[0]['metric']['beta']
  print('52 Week High:','$',meta_data1)
  print('52 Week Low & Date:','$',meta_data2,',', meta_data3)
  print('52 Week Percent change:',round(meta_data4, 2),'%')
  print('Beta:',round(meta_data5, 2))
  # Include Yahoo Finance URL
  print('See more on Yahoo Finance:',f"https://finance.yahoo.com/quote/{ticker}/") # ticker is the varibale used above
  return current_price, meta_data1, meta_data2, meta_data3, meta_data4, meta_data5
# Example usage:
#ticker_meta_data(f'{ticker}')