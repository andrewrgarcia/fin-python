# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 23:09:48 2019

@author: garci
"""
'''
Adapted from: How to Download Historical Price Data from Binance with Python
marketstack (62) in python •  9 months ago

https://steemit.com/python/@marketstack/how-to-download-historical-price-data-from-binance-with-python
'''


import requests        # for making http requests to binance
import json            # for parsing what binance sends back to us
import pandas as pd    # for storing and manipulating the data we get back
import numpy as np     # numerical python, i usually need this somewhere
                       # and so i import by habit nowadays

import matplotlib.pyplot as plt # for charts and such

import datetime as dt  # for dealing with times


'''
KLINE_INTERVAL_1MINUTE = '1m'
KLINE_INTERVAL_3MINUTE = '3m'
KLINE_INTERVAL_5MINUTE = '5m'
KLINE_INTERVAL_15MINUTE = '15m'
KLINE_INTERVAL_30MINUTE = '30m'
KLINE_INTERVAL_1HOUR = '1h'
KLINE_INTERVAL_2HOUR = '2h'
KLINE_INTERVAL_4HOUR = '4h'
KLINE_INTERVAL_6HOUR = '6h'
KLINE_INTERVAL_8HOUR = '8h'
KLINE_INTERVAL_12HOUR = '12h'
KLINE_INTERVAL_1DAY = '1d'
KLINE_INTERVAL_3DAY = '3d'
KLINE_INTERVAL_1WEEK = '1w'
KLINE_INTERVAL_1MONTH = '1M
'''

#INTERVAL = '1d'
INTERVAL = '4h'

def get_bars(symbol, interval = INTERVAL):
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


def coindoll(symbol, interval = INTERVAL):

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
