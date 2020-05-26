# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 11:54:40 2018

@author: garci
"""
'''backtest_simple.py : Core code for backtesting analysis with stock and
cryptocurrencies importing capabilities from IEX and Binance, respectivelyself.
Andrew Garcia 2018-2020

Adapted from: published codes from "Python for Finance" (Yves Hilpisch, 2014)
2020 Update: API for crypto remains Binance, API for stocks [free]: yahoofinance
'''

import numpy as np
import pandas as pd

import pandas_datareader.data as web
import datetime as dt
#from cryptoreader import *
from binancereader import *
#from plotly_plots import plyfin
from andrewsticks import chart, chart_stock

#import os
#api = 
from iexfinance.stocks import Stock
import matplotlib.pyplot as plt
from iexfinance.stocks import get_historical_data

import yfinance as yf

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--epochs", 
                default = 500,
                type = int, help="number of iterations (or epochs)")
ap.add_argument("-n", "--ticker_name", 
                default = 'BTC', 
                type =str, help="ticker name for equity")
ap.add_argument("-s", "--strategy", 
                default = 'buylowsellhigh', 
                type =str, help="trading strategy")
ap.add_argument("-c", "--crypto_option", 
                default = 'y',
                type=str, help="Cryptocurrency?[y] or stock [n] (default:'y')")

args = vars(ap.parse_args())



'moving averages to compare against'
MA1 = 12
MA2 = 26

'tolerance for moving avg. comparison / regime determination'
SD = 0

'''# ==================== STOCK PARAMETERS GO HERE ========================='''


'beginning date of data collection'
start = dt.datetime(2020, 3, 16)
'end date'
end = dt.datetime.now()


'''# ========== CRYPTOCURRENCIES PARAMETERS GO HERE ============='''

intl='1d'

'''# ======================================================================='''

'''for data not present in Remote Data Access sources (iex, quandl, morningstar),
uncomment lines below / make code modifications'''

    
close_str = 'Close' if args["crypto_option"] is 'n' else 'close'

if args["crypto_option"] is 'y':
    hist_data = coindoll(args["ticker_name"],interval = intl,weight='USDT')

else:
    
    'IEX expensive'
#    hist_data = web.DataReader(args["ticker_name"], 'iex', start, end)
#    hist_data = getHistoricalPrices(args["ticker_name"]_STOCKS,start,end)
    stock = yf.Ticker(args["ticker_name"])
    hist_data = stock.history(interval='1h',\
                              start=start.strftime("%Y-%m-%d"),end=end.strftime("%Y-%m-%d"))
    print(hist_data)

#    print(hist_data)

''' Historical data with moving averages '''
#print(hist_data)

#print(hist_data.index)

#hist_data[[close_str]].plot(title = '{} Historical Data'.format(args["ticker_name"]), grid=False, figsize=(8, 5))

hist_data[str(MA1)+' fast length'] = hist_data[close_str].rolling(window=MA1).mean()
hist_data[str(MA2)+' slow length'] = hist_data[close_str].rolling(window=MA2).mean()

hist_data[[close_str, str(MA1)+' fast length', str(MA2)+' slow length']].tail()


''' buy / sell / hold regime determination '''
hist_data['MACD'] = hist_data[str(MA1)+' fast length'] - hist_data[str(MA2)+' slow length']

MACD = hist_data['MACD']

dM = np.array([(MACD[i] - MACD[i-1]) for i in range(len(MACD))])
#ddMp = np.array([(dM[i] - dM[i-1]) for i in range(len(MACD))])
#ddMn = np.array([(dM[i])/dM[i-1] for i in range(len(MACD))])

'strategy'

if args["strategy"] is 'buylowsellhigh':

    hist_data['regime'] = np.where(MACD > SD,1,0)
    hist_data['regime'] = np.where(MACD < -SD,-1,hist_data['regime'])



hist_data['regime'].value_counts()
#    hist_data['regplot']=max(hist_data[close_str])*(2+hist_data['regime'])/8
#hist_data['regplot']=(hist_data[close_str].iloc[-1])*(100+5*hist_data['regime'])/100

#hist_data['buy hold sell']=max(hist_data[close_str])*(100+5*hist_data['regime'])/100
hist_data['buy hold sell']=hist_data['regime']



'''Market / Strategy comparison '''

hist_data['market'] = np.log(hist_data[close_str] / hist_data[close_str].shift(1))

#hist_data['strategy'] =  hist_data['market'] *(1+hist_data['regime'].shift(1))
hist_data['strategy'] =  hist_data['regime'].shift(1) * hist_data['market']

'''include Capital Gains tax for sold equities'''
#taxrate=0.2
#LS = len(hist_data['market'])
#
#capgains = 0
#for i in range(LS):
#
#    if hist_data['regime'][i] == 1 and hist_data['regime'][(i+2)%LS] == -1:
#
#        X_sell = hist_data['strategy'].cumsum().iloc[i+2] - hist_data['market'].cumsum().iloc[i+2]
#        taxed_sale = X_sell*taxrate
#        print(taxed_sale)
#        capgains += taxed_sale

'''plot treatment -  final details'''


hist_data[['market','strategy']]=hist_data[['market','strategy']].cumsum().apply(np.exp)

X=hist_data['strategy'].cumsum().iloc[-1] - hist_data['market'].cumsum().iloc[-1]

print('final data pt. difference b/t market & strat: ',X)

'plot.ly: to public cloud'
#plyfin(hist_data,args["ticker_name"],MA1,MA2,crypto)
import matplotlib.dates as mdates

def makeplt():
#    datenow = datetime.datetime.now()
#    tit = str(datenow)
    tit= ' Strategy: Buy MACD > 0 Sell MACD < 0 ({})'.format(args["ticker_name"])  if args["strategy"] is 'buylowsellhigh' \
    else None
    
    if args["crypto_option"] is 'n':
        chart_stock(hist_data,curr=args["ticker_name"], invl='1d', weight='USDT',MAv1=MA1,MAv2=MA2,tol='',\
              title=tit,xaxis='')
    else:
        chart(hist_data,curr=args["ticker_name"], invl=intl, weight='USDT',MAv1=MA1,MAv2=MA2,tol='',\
              title=tit,xaxis='')
        

makeplt()

