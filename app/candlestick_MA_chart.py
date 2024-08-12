# THIS code adds rolling 50-day and 200-day moving averages to a candlestick chart

import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
load_dotenv()

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

    # Sort by Date
    df1.sort_values(by='Date', inplace=True)

    # Calculate moving averages
    df1['MA50'] = df1['Close'].rolling(window=50, min_periods=1).mean()
    df1['MA200'] = df1['Close'].rolling(window=200, min_periods=1).mean()

    # Create the candlestick figure
    fig = go.Figure(data=[go.Candlestick(
        x=df1['Date'],
        open=df1['Open'],
        high=df1['High'],
        low=df1['Low'],
        close=df1['Close']
    )])

    # Add moving averages to the figure
    fig.add_trace(go.Scatter(
        x=df1['Date'],
        y=df1['MA50'],
        mode='lines',
        name='50-day MA',
        line=dict(color='blue', width=1)
    ))

    fig.add_trace(go.Scatter(
        x=df1['Date'],
        y=df1['MA200'],
        mode='lines',
        name='200-day MA',
        line=dict(color='red', width=1)
    ))

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