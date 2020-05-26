# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:58:54 2019

@author: garci
"""
'''andrewsticks.py : A script for making candlestick charts from OHLC data
exported from Binance exchange
Andrew Garcia 2019-2020'''


from mpl_finance import candlestick2_ohlc
from mpl_finance import candlestick_ohlc


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as datetime
import numpy as np
import binancereader as brc

import matplotlib.dates as mdates

datenow = datetime.datetime.now()
plt.style.use('fivethirtyeight')

def chart(data, curr='BTC', invl='1M', weight='USDT',MAv1=0,MAv2=0,tol='',\
          title=str(datenow),xaxis='',c_up='dodgerblue',c_dn='pink',c_ma1='magenta',c_ma2='blue'):
    
    
    quotes = brc.coindoll(curr, invl,weight)
    
#    fig, ax = plt.subplots()
    fig, (ax, ax2,ax3,ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios':[4,2,2,1]})

    
    time = mdates.epoch2num(quotes['open_time']*1e-3 - 14400)
    new= zip(time, \
             quotes['open'],quotes['high'],quotes['low'],quotes['close'])
    
    'define bar width'
    wadth0 = 0.02
    wadth = 0.02 if invl == '1h' \
                     else wadth0*int(invl[:-1])/60 if invl[-1:] == 'm' \
                     else wadth0*int(invl[:-1]) if invl[-1:] == 'h' \
                     else wadth0*24*int(invl[:-1]) if invl[-1:] == 'd' \
                     else wadth0*24*7*int(invl[:-1]) if invl[-1:] == 'w' \
                     else wadth0*24*7*4*int(invl[:-1]) if invl[-1:] == 'M' \
                     else 0.001
                     
    candlestick_ohlc(ax,new, width= wadth, colorup=c_up, colordown=c_dn)

    m1=quotes['close'].rolling(MAv1).mean()
    m2=quotes['close'].rolling(MAv2).mean()
    if MAv1 != 0 and MAv2 != 0:
        ax.plot(time,m1,label='MA {}'.format(MAv1),color=c_ma1,linewidth=1)
        ax.plot(time,m2,label='MA {}'.format(MAv2),color=c_ma2,linewidth=1)
        ax.legend(title='tol: '+tol if tol !='' else None)
        
        diff=(m1-m2)
        nordiff = (m1-m2)/np.max(abs(diff))
        ax3.bar(time,diff,width=wadth*1.5,color=(diff > 0).map({True: 'dodgerblue', False: 'grey'}) )
#        ax3.get_yaxis().set_visible(False)
        ax2.plot(time,data['strategy'],linewidth=1,label='strategy')
        ax2.plot(time,data['market'],linewidth=1,label='market')
        ax2.legend()

        ax4.plot(time,data['buy hold sell'],color='crimson',linewidth=1,label='regime')
        ax4.legend()

        
        
        
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()
    fig.subplots_adjust(hspace=0)

    ax.set_ylabel(curr+'USDT' if weight == 'USDT' else curr+'BTC', size=14)
    ax.set_xlabel(xaxis)
    ax.set_title(title)

     
def chart_stock(data, curr='BTC', invl='1M', weight='USDT',MAv1=0,MAv2=0,tol='',\
          title=str(datenow),xaxis='',c_up='dodgerblue',c_dn='pink',c_ma1='magenta',c_ma2='blue'):
    
    
    quotes = data
    close_str = 'Close'
    
#    fig, ax = plt.subplots()
    fig, (ax, ax2,ax3,ax4) = plt.subplots(4, 1, sharex=True,gridspec_kw={'height_ratios':[4,2,2,1]})

    
    time = mdates.date2num(quotes.index)
    
    new= zip(time, \
             quotes['Open'],quotes['High'],quotes['Low'],quotes['Close'])
    
    'define bar width'
    wadth0 = 0.02
    wadth = 0.02 if invl == '1h' \
                     else wadth0*int(invl[:-1])/60 if invl[-1:] == 'm' \
                     else wadth0*int(invl[:-1]) if invl[-1:] == 'h' \
                     else wadth0*24*int(invl[:-1]) if invl[-1:] == 'd' \
                     else wadth0*24*7*int(invl[:-1]) if invl[-1:] == 'w' \
                     else wadth0*24*7*4*int(invl[:-1]) if invl[-1:] == 'M' \
                     else 0.001
                     
    candlestick_ohlc(ax,new, width= wadth, colorup=c_up, colordown=c_dn)

    m1=quotes[close_str].rolling(MAv1).mean()
    m2=quotes[close_str].rolling(MAv2).mean()
    if MAv1 != 0 and MAv2 != 0:
        ax.plot(time,m1,label='MA {}'.format(MAv1),color=c_ma1,linewidth=1)
        ax.plot(time,m2,label='MA {}'.format(MAv2),color=c_ma2,linewidth=1)
        ax.legend(title='tol: '+tol if tol !='' else None)
        
        diff=(m1-m2)
        nordiff = (m1-m2)/np.max(abs(diff))
        ax3.bar(time,diff,width=wadth*1.5,color=(diff > 0).map({True: 'dodgerblue', False: 'grey'}) )
#        ax3.get_yaxis().set_visible(False)
        ax2.plot(time,data['strategy'],linewidth=1,label='strategy')
        ax2.plot(time,data['market'],linewidth=1,label='market')
        ax2.legend()

        ax4.plot(time,data['buy hold sell'],color='crimson',linewidth=1,label='regime')
        ax4.legend()

        
        
        
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()
    fig.subplots_adjust(hspace=0)

    ax.set_ylabel(curr, size=14)
    ax.set_xlabel(xaxis)
    ax.set_title(title)    
