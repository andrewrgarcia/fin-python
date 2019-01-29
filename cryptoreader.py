# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 15:00:06 2018

@author: garci

adapted from: ANALYZING CRYPTOCURRENCY MARKETS USING PYTHON
Python, Data Science, Guides | 20 AUGUST 2017
A DATA-DRIVEN APPROACH

https://blog.patricktriest.com/analyzing-cryptocurrencies-python/
"""
import os
import numpy as np
import pandas as pd
import pickle
import datetime as dt



def get_json_data(json_url, cache_path):
    '''Download and cache JSON data, return as a dataframe.'''
    try:        
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(json_url))
    except (OSError, IOError) as e:
        print('Downloading {}'.format(json_url))
        df = pd.read_json(json_url)
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(json_url, cache_path))
    return df

base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
#start = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
start = dt.datetime(2018,6, 1)

end = dt.datetime.now() # up until today
#end = dt.datetime(2017,10, 1) # up until today

pediod = 86400 # pull daily data (86,400 seconds per day)

def get_crypto_data(start,end,poloniex_pair):
    '''Retrieve cryptocurrency data from poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start.timestamp(), end.timestamp(), pediod)
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')
    return data_df

altcoins = ['ETH','LTC','XRP','ETC','STR','DASH','SC','XMR','XEM','DOGE']

altcoin_data = {}
for altcoin in altcoins:
    coinpair = 'BTC_{}'.format(altcoin)
    crypto_price_df = get_crypto_data(start,end,coinpair)
    altcoin_data[altcoin] = crypto_price_df
   
    
get_crypto_data(start,end,'BTC_ETH')