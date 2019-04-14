# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 11:54:40 2018

@author: garci
"""
'''backtest_simple.py : Core code for backtesting analysis with stock and
cryptocurrencies importing capabilities from IEX and Binance, respectivelyself.
Andrew Garcia 2018-2019

Adapted from: published codes from "Python for Finance" (Yves Hilpisch, 2014)
'''

import numpy as np
import pandas as pd

import pandas_datareader.data as web
import datetime as dt
#from cryptoreader import *
from binancereader import *


'''# ==================== STOCK PARAMETERS GO HERE ========================='''

ticker_name='SBUX'

'moving averages to compare against'
roll_mean1 = 21
roll_mean2 = 63

'tolerance for moving avg. comparison / regime determination'
SD = 0.01

'''# ========== CRYPTOCURRENCIES (Boolean to True, else False) ============='''
crypto = True

ticker_name = 'BNB'

'''# ======================================================================='''

'''for data not present in Remote Data Access sources (iex, quandl, morningstar),
uncomment lines below / make code modifications'''
#hist_data = pd.read_csv(ticker_name+'.csv')
#hist_data.info()
#
#hist_data[['date','Close']].plot(title = ticker_name, x='date', grid=False, figsize=(8, 5))



'beginning date of data collection'
start = dt.datetime(2017, 1, 1)
'end date'
end = dt.datetime.now()

close_str = 'close'

if crypto == True:
    hist_data = coindoll(ticker_name)

else:

    hist_data = web.DataReader(ticker_name, 'iex', start, end)


''' Historical data with moving averages '''


print(hist_data)
#print(hist_data.index)

#hist_data[[close_str]].plot(title = '{} Historical Data'.format(ticker_name), grid=False, figsize=(8, 5))


hist_data[str(roll_mean1)+'d'] = np.round(pd.rolling_mean(hist_data[close_str], window=roll_mean1), 2)
hist_data[str(roll_mean2)+'d'] = np.round(pd.rolling_mean(hist_data[close_str], window=roll_mean2), 2)

hist_data[[close_str, str(roll_mean1)+'d', str(roll_mean2)+'d']].tail()

hist_data[[close_str, str(roll_mean1)+'d', str(roll_mean2)+'d']].plot(grid=False, figsize=(8, 5))



''' buy / sell / hold regime determination '''

hist_data['mov_avg'] = hist_data[str(roll_mean1)+'d'] - hist_data[str(roll_mean2)+'d']

hist_data['mov_avg'].tail()

hist_data['regime'] = np.where(hist_data['mov_avg'] > SD, 1, 0)
hist_data['regime'] = np.where(hist_data['mov_avg'] < -SD, -1, hist_data['regime'])
hist_data['regime'].value_counts()

hist_data['regplot']=max(hist_data[close_str])*(100+hist_data['regime'])/100
hist_data['regplot'].plot(title= '{} technical analysis'.format(ticker_name),linestyle='--',  grid=False,lw=1.5)



'''Market / Strategy comparison '''

hist_data['market'] = np.log(hist_data[close_str] / hist_data[close_str].shift(1))

hist_data['strategy'] =  hist_data['market'] *(1+hist_data['regime'].shift(1))

'''include Capital Gains tax for sold equities'''
taxrate=0.2
LS = len(hist_data['market'])

capgains = 0
for i in range(LS):

    if hist_data['regime'][i] == 1 and hist_data['regime'][(i+2)%LS] == -1:

        X_sell = hist_data['strategy'].cumsum().iloc[i+2] - hist_data['market'].cumsum().iloc[i+2]
        taxed_sale = X_sell*taxrate
        print(taxed_sale)
        capgains += taxed_sale

'''plot treatment -  final details'''


#hist_data[['market','strategy']].cumsum().apply(np.exp).\
#plot(title='{} Market v. Strategy Return comparison'.format(ticker_name),grid=False, figsize=(8, 5))
hist_data[['market','strategy']]=hist_data[['market','strategy']].cumsum().apply(np.exp)
hist_data[['market','strategy']].plot(title='{} Market v. Strategy Return comparison'.format(ticker_name),grid=False, figsize=(8, 5))


X=hist_data['strategy'].cumsum().iloc[-1] - hist_data['market'].cumsum().iloc[-1]

print('final data pt. difference b/t market & strat: ',X)





'''PLOTLY (to public cloud)'''
from plotly_cred import info

import plotly
plotly.tools.set_credentials_file(username=info()[0], api_key=info()[1])
import plotly.plotly as py
import plotly.graph_objs as go

'PLOT # 1: Stock Price, Moving Averages and Buy-Sell Regimes'

if crypto == False:

    trace = go.Ohlc(x=hist_data.index,
                    open=hist_data['open'],
                    high=hist_data['high'],
                    low=hist_data['low'],
                    close=hist_data[close_str])
    
if crypto == True:

    trace = go.Ohlc(x=hist_data.index,
                    open=hist_data['o'],
                    high=hist_data['h'],
                    low=hist_data['l'],
                    close=hist_data['close'],
                    name = 'candlesticks')

trace2 = go.Scatter(x=hist_data.index,
                    y=hist_data[str(roll_mean1)+'d'],
                    name = 'moving average trend')

trace3 = go.Scatter(x=hist_data.index,
                    y=hist_data[str(roll_mean2)+'d'],
                    name = 'moving average baseline')

trace4 = go.Scatter(x=hist_data.index,
                    y=hist_data['regplot'],
                    name = 'buy-hodl-sell regimes')

data = [trace,trace2,trace3,trace4]

layout=go.Layout(title=ticker_name+' Equity', xaxis={'title':'Date'}, yaxis={'title':''})
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename=ticker_name+' Equity')


'PLOT # 2: Backtesting Strategy Assessment'
trce1 = go.Scatter(x=hist_data.index,
                   y=hist_data['market'],
                   name ='market value')
trce2 = go.Scatter(x=hist_data.index,
                   y=hist_data['strategy'],
                   name ='strategy value')

data= [trce1,trce2]
layout=go.Layout(title=ticker_name+' Strategy Assessment', xaxis={'title':'Date'}, yaxis={'title':''})
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename=ticker_name+' Strategy Assessment')
