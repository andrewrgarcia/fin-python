# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 23:09:48 2019

@author: garci

adapted from: How to Download Historical Price Data from Binance with Python
marketstack (62) in python •  9 months ago

https://steemit.com/python/@marketstack/how-to-download-historical-price-data-from-binance-with-python

"""

import requests        # for making http requests to binance
import json            # for parsing what binance sends back to us
import pandas as pd    # for storing and manipulating the data we get back
import numpy as np     # numerical python, i usually need this somewhere
                       # and so i import by habit nowadays

import matplotlib.pyplot as plt # for charts and such

import datetime as dt  # for dealing with times

#intrl = '1d'
intrl = '4h'

def get_bars(symbol, interval = intrl):
   root_url = 'https://api.binance.com/api/v1/klines'
   url = root_url + '?symbol=' + symbol + '&interval=' + interval
   data = json.loads(requests.get(url).text)
   df = pd.DataFrame(data)
   df.columns = ['open_time',
                 'o', 'h', 'l', 'c', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
   df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]

   return df


def coindoll(symbol, interval = intrl):

    if symbol == 'BTC':
        df = get_bars('BTCUSDT', interval = interval)
        df['close'] = df['c'].astype('float')
    else:
        df = get_bars(symbol + 'BTC', interval = interval)

        coinbtc = df['c'].astype('float')
        btcusd = get_bars('BTCUSDT', interval = interval)['c'].astype('float')
        transform = coinbtc *btcusd
        df['close'] = transform


    return df

#print(coindoll('BTC'))
#print(coindoll('ETH'))
