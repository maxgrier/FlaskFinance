from flask import Flask, render_template
# from flask import request, redirect, url_for
# from matplotlib import pyplot as plt
# from mpld3 import plugins
import pandas as pd
from pandas import DataFrame
# import time
import yfinance as yf

import json
import plotly
import numpy as np


app = Flask(__name__)

# Possible panda columns
pc = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']

# Arrays to store each index's total price information for Flask
sp_total_data = []
dow_total_data = []
nasdaq_total_data = []

# Define ticker symbols
tickers = ['SPY', 'DIA', 'QQQ']
prefixes = ['sp', 'dow', 'nasdaq']
sp_index = 'SPY'
dow_index = 'DIA'
nasdaq_index = 'QQQ'

# Add graph id's
ids = ['SPY', 'DIA', 'QQQ']

# Get the data on the tickers
sp_data = yf.Ticker(sp_index)
dow_data = yf.Ticker(dow_index)
nasdaq_data = yf.Ticker(nasdaq_index)

# Get the historical prices for the ticker
sp_price = sp_data.history(period='30d')
dow_price = dow_data.history(period='30d')
nasdaq_price = nasdaq_data.history(period='30d')

# Reset indexes to allow for the graph to use date on x axis
sp_price.reset_index(inplace=True)
dow_price.reset_index(inplace=True)
nasdaq_price.reset_index(inplace=True)

# print("price", sp_price)
# print("date", sp_price)
# print(sp_price['Date'])

# Set the S&P data variables for the graph from the data frame
sp_df = DataFrame(sp_price, columns=['Date', 'High'])
sp_df.plot(x='Date', y='High', kind='line')

# Set the Dow data variables for the graph from the data frame
dow_df = DataFrame(sp_price, columns=['Date', 'High'])
dow_df.plot(x='Date', y='High', kind='line')

# Set the NASDAQ data variables for the graph from the data frame
nasdaq_df = DataFrame(sp_price, columns=['Date', 'High'])
nasdaq_df.plot(x='Date', y='High', kind='line')

i = 0
while i < len(pc):
    # print(pc[i])
    # print(sp_price[pc[i]][1])
    # print('------')
    sp_total_data.append(sp_price[pc[i]][1])
    dow_total_data.append(dow_price[pc[i]][1])
    nasdaq_total_data.append(nasdaq_price[pc[i]][1])
    i += 1
# print('total sp data', sp_total_data)


@app.route('/')
def index():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    # Set up the graphs for the site
    graphs = [
        # S&P graph data
        dict(data=[dict(x=sp_price['Date'], y=sp_price['High'], type='line'), ], layout=dict(title=ids[0])),

        # Dow graph
        dict(data=[dict(x=dow_price['Date'], y=dow_price['High'], type='line'), ], layout=dict(title=ids[1])),

        # NASDAQ graph
        # Can use the pandas data structures directly
        # dict(data=[dict(x=ts.index, y=ts)])]

        dict(data=[dict(x=nasdaq_price['Date'], y=nasdaq_price['High'], type='line'), ], layout=dict(title=ids[2]))
            ]

        # Add "ids" to each of the graphs to pass up to the client for templating
    # old "graph-0" fromat
    # ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', ids=ids, graphJSON=graphJSON,
                           sp_total_data=sp_total_data, dow_total_data=dow_total_data,
                           nasdaq_total_data=nasdaq_total_data, tickers=tickers, prefixes=prefixes)


# Route I was using and works ok
# def send_data():
#     return render_template('index.html', sp_total_data=sp_total_data, tickers=tickers,
#                            plot=plot)

# @app.route('/', methods=['POST'])
# def search():
#     ticker = request.form['ticker_symbol']
#
#     ts = TimeSeries(key=api_key, output_format='pandas')
#     data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
#
#     # close_data = str(data['4. close'][1])
#     # close_data = tuple(data)
#
#     # new_data = []
#     #
#     # new_data.append(close_data)
#
#     # Set variables based on panda output
#     price_date_data = str(data.index[0]).split(" ")
#     price_date = price_date_data[0]
#     price_time = price_date_data[1]
#
#     open_price = str(data['1. open'][1])
#     high_price = str(data['2. high'][1])
#     low_price = str(data['3. low'][1])
#     close_price = str(data['4. close'][1])
#     volume = str(data['5. volume'][1])
#
#     price_data = (open_price, high_price, low_price, close_price, volume)
#
#
#     print(ticker)
#     return render_template('index.html', content=price_data, symbol=ticker, time_data=price_date_data)
#


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0') #, port = 5000)
