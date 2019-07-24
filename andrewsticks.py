# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:58:54 2019

@author: garci
"""
'''andrewsticks.py : A script for making candlestick charts from OHLC data
exported from Binance exchange
Andrew Garcia 2019'''


from mpl_finance import candlestick2_ohlc
from mpl_finance import candlestick_ohlc


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as datetime
import numpy as np
import binancereader as brc

import matplotlib.dates as mdates

def chart(curr='BTC', invl='1M', weight='USDT',mano1=0,mano2=0,tol='',\
          title=str(datetime.datetime.now()),xaxis=''):
    
    quotes = brc.coindoll(curr, invl,weight)
    
    fig, ax = plt.subplots()
    
    time = mdates.epoch2num(quotes['open_time']*1e-3 - 14400)
    new= zip(time, \
             quotes['open'],quotes['high'],quotes['low'],quotes['close'])
    
    
    wadth = 0.02
    candlestick_ohlc(ax,new,\
                     width= wadth if invl == '1h' \

                     else wadth*int(invl[:-1])/60 if invl[-1:] == 'm' \
                     else wadth*int(invl[:-1]) if invl[-1:] == 'h' \
                     else wadth*24*int(invl[:-1]) if invl[-1:] == 'd' \
                     else wadth*24*7*int(invl[:-1]) if invl[-1:] == 'w' \
                     else wadth*24*7*4*int(invl[:-1]) if invl[-1:] == 'M' \
                     else 0.001,\
                     colorup='dodgerblue', colordown='#CD919E')
#                     colorup='dodgerblue', colordown='gray')

    
    ma1=quotes['close'].rolling(mano1).mean()
    ma2=quotes['close'].rolling(mano2).mean()
    if mano1 != 0 and mano2 != 0:
        plt.plot(time,ma1,label='MA {}'.format(mano1),color='m',linewidth=1)
        plt.plot(time,ma2,label='MA {}'.format(mano2),color='k',linewidth=1)
        plt.legend(title='tol: '+tol if tol !='' else None)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()

    plt.ylabel('BINANCE: '+curr+'USDT' if weight == 'USDT' else 'BINANCE: '+curr+'BTC', size=14)
    plt.xlabel(xaxis)
    #plt.ylabel('$'+curr+'\)
    plt.title(title)
    fig.tight_layout()
    plt.show()
    
    
#chart(invl='1m')
