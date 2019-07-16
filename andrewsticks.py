# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:58:54 2019

@author: garci
"""
from mpl_finance import candlestick2_ohlc
from mpl_finance import candlestick_ohlc



import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as datetime
import numpy as np
import binancereader as brc

import matplotlib.dates as mdates

def chart(curr='BTC', invl='1M', rate='USDT',mano1=0,mano2=0,tol=''):
    #curr, invl, rate = 'BTC', '1h', 'b'
    
    quotes = brc.coindoll(curr, invl,rate)
    
    fig, ax = plt.subplots()
    
    time = mdates.epoch2num(quotes['open_time']*1e-3 - 14400)
    new= zip(time, \
             quotes['open'],quotes['high'],quotes['low'],quotes['close'])
    
    
    candlestick_ohlc(ax,new,\
                     width= 0.5 if invl == '1d' \
                     else 10 if invl == '1M'\
                     else 0.08 if invl == '4h' \
                     else 0.02 if invl == '1h' \
                     else 0.0003 if invl == '1m' \
                     else 0.001,colorup='dodgerblue', colordown='#CD919E')
    
    ma1=quotes['close'].rolling(mano1).mean()
    ma2=quotes['close'].rolling(mano2).mean()
    if mano1 != 0 and mano2 != 0:
        plt.plot(time,ma1,label='MA {}'.format(mano1),color='m',linewidth=1)
        plt.plot(time,ma2,label='MA {}'.format(mano2),color='k',linewidth=1)
        plt.legend(title='tol: '+tol if tol !='' else None)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.ylabel('BINANCE: '+curr+'USDT' if rate == 'USDT' else 'BINANCE: '+curr+'BTC', size=14)
    #plt.ylabel('$'+curr+'\)
    
    plt.show()
    
chart()
#chart(curr='BTC', invl='1h', rate='b',mano1=11,mano2=22)