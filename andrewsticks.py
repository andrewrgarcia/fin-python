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

datenow = datetime.datetime.now()

def chart(curr='BTC', invl='1M', weight='USDT',MAv1=0,MAv2=0,tol='',\
          title=str(datenow),xaxis='',c_up='darkgray',c_dn='navy',c_ma1='blue',c_ma2='red'):
    
    
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
                     colorup=c_up, colordown=c_dn)
#                     colorup='dodgerblue', colordown='gray')

    m1=quotes['close'].rolling(MAv1).mean()
    m2=quotes['close'].rolling(MAv2).mean()
    if MAv1 != 0 and MAv2 != 0:
        plt.plot(time,m1,label='MA {}'.format(MAv1),color=c_ma1,linewidth=1)
        plt.plot(time,m2,label='MA {}'.format(MAv2),color=c_ma2,linewidth=1)
        plt.legend(title='tol: '+tol if tol !='' else None)
    
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()

    plt.ylabel('BINANCE: '+curr+'USDT' if weight == 'USDT' else 'BINANCE: '+curr+'BTC', size=14)
    plt.xlabel(xaxis)
    #plt.ylabel('$'+curr+'\)
    plt.title(title)
#    fig.tight_layout()
#    plt.show()
    
    
chart(invl='1h')
