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
#from plotly_plots import plyfin
from andrewsticks import chart


'moving averages to compare against'
MA1 = 12
MA2 = 17

'tolerance for moving avg. comparison / regime determination'
SD = 0.1

'''# ==================== STOCK PARAMETERS GO HERE ========================='''

ticker_name='SBUX'


'beginning date of data collection'
start = dt.datetime(2017, 1, 1)
'end date'
end = dt.datetime.now()


'''# ========== CRYPTOCURRENCIES (Boolean to True, else False) ============='''

crypto = True

ticker_name = 'BTC'

intl='1h'

'''# ======================================================================='''

'''for data not present in Remote Data Access sources (iex, quandl, morningstar),
uncomment lines below / make code modifications'''
#hist_data = pd.read_csv(ticker_name+'.csv')
#hist_data.info()
#
#hist_data[['date','Close']].plot(title = ticker_name, x='date', grid=False, figsize=(8, 5))





close_str = 'close'

if crypto == True:
    hist_data = coindoll(ticker_name,interval = intl,weight='USDT')

else:

    hist_data = web.DataReader(ticker_name, 'iex', start, end)


''' Historical data with moving averages '''


print(hist_data)

#print(hist_data.index)

#hist_data[[close_str]].plot(title = '{} Historical Data'.format(ticker_name), grid=False, figsize=(8, 5))


#hist_data[str(MA1)+'d MA'] = np.round(pd.rolling_mean(hist_data[close_str], window=MA1), 2)
#hist_data[str(MA2)+'d MA'] = np.round(pd.rolling_mean(hist_data[close_str], window=MA2), 2)
hist_data[str(MA1)+'d MA'] = hist_data[close_str].rolling(window=MA1).mean()
hist_data[str(MA2)+'d MA'] = hist_data[close_str].rolling(window=MA2).mean()

hist_data[[close_str, str(MA1)+'d MA', str(MA2)+'d MA']].tail()


''' buy / sell / hold regime determination '''

hist_data['mov_avg'] = hist_data[str(MA1)+'d MA'] - hist_data[str(MA2)+'d MA']

hist_data['mov_avg'].tail()

hist_data['regime'] = np.where(hist_data['mov_avg'] > SD, 1, 0)
hist_data['regime'] = np.where(hist_data['mov_avg'] < -SD, -1, hist_data['regime'])
hist_data['regime'].value_counts()

#hist_data['buy hold sell']=max(hist_data[close_str])*(100+hist_data['regime'])/100
hist_data['buy hold sell']=max(hist_data[close_str])*(100+5*hist_data['regime'])/100



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

hist_data['strategy return'] = hist_data['strategy']*hist_data[close_str]


X=hist_data['strategy'].cumsum().iloc[-1] - hist_data['market'].cumsum().iloc[-1]

print('final data pt. difference b/t market & strat: ',X)

'plot.ly: to public cloud'
#plyfin(hist_data,ticker_name,MA1,MA2,crypto)



def oldplt():
    hist_data[[close_str, str(MA1)+'d MA', str(MA2)+'d MA']].plot(grid=False)
    hist_data['buy hold sell'].plot(title= '{} technical analysis'.format(ticker_name),linestyle='--',  grid=False,lw=1.5)
    hist_data['strategy return'].plot()
    plt.legend()

import matplotlib.dates as mdates
def newplt():
    datenow = datetime.datetime.now()
    chart(curr=ticker_name, invl=intl, weight='USDT',MAv1=MA1,MAv2=MA2,tol='',\
              title=str(datenow),xaxis='')
    
    quotes = coindoll(ticker_name, intl,weight='USDT')
    time = mdates.epoch2num(quotes['open_time']*1e-3 - 14400)
    plt.plot(time,hist_data['strategy return'],linewidth=1,label='strategy')
    plt.plot(time,hist_data['buy hold sell'],color='lightgray',linewidth=1,label='buy-hold-sell lines')
#    plt.suptitle('Technical analysis')
    plt.legend()


newplt()

