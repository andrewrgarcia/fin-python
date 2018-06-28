# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 11:54:40 2018

@author: garci
"""

import numpy as np
import pandas as pd

import pandas_datareader.data as web
import datetime as dt

import comm_pars
'''comm_pars.py: returns ticker name (as a string) of commodity, 
rolling means 1 and 2 and SD (as numbers) from vector def
e.g. def Netflix:
        #return [TICKER NAME, interval for moving average 1," " moving average 2 , SD('tolerance')]
        return ['NFLX',42,365,5]
will not push this stock_params.py; personal stock info'''


def qtech( commodity = comm_pars.Funko() ):
    
    'beginning date of data collection'
    start = dt.datetime(2015, 1, 1)
    'end date'
    end = dt.datetime.now()
    
    name, roll_mean1,roll_mean2, SD = commodity
    'or if inputting values  manually ; uncomment line 31, comment out line 29:'
#    name, roll_mean1,roll_mean2, SD = 'TSLA', 21, 24, 5
    
    
    hist_data = web.DataReader(name, 'morningstar', start, end)
    
    print(hist_data)

    '''for data not present in NASDAQ (i.e. coins) need to uncomment lines / make 
    code modifications''' 
#    hist_data = pd.read_csv(name+'.csv')
#    hist_data.info()
    
#    hist_data[['date','close']].plot(title = name, x='date', grid=False, figsize=(8, 5))
    hist_data[['Close']].plot(title = name, grid=False, figsize=(8, 5))

    
   
    ''' Historical data with moving averages '''
    
    hist_data[str(roll_mean1)+'d'] = np.round(pd.rolling_mean(hist_data['Close'], window=roll_mean1), 2)
    hist_data[str(roll_mean2)+'d'] = np.round(pd.rolling_mean(hist_data['Close'], window=roll_mean2), 2)
    
    hist_data[['Close', str(roll_mean1)+'d', str(roll_mean2)+'d']].tail()
    
#    hist_data[['date','close', str(roll_mean1)+'d', str(roll_mean2)+'d']].plot(x='date',grid=False, figsize=(8, 5))
    hist_data[['Close', str(roll_mean1)+'d', str(roll_mean2)+'d']].plot(grid=False, figsize=(8, 5))

    
    '''regime det. '''
    
    hist_data['42-252'] = hist_data[str(roll_mean1)+'d'] - hist_data[str(roll_mean2)+'d']
    
    hist_data['42-252'].tail()
    
    hist_data['regime'] = np.where(hist_data['42-252'] > SD, 1, 0)
    hist_data['regime'] = np.where(hist_data['42-252'] < -SD, -1, hist_data['regime'])
    hist_data['regime'].value_counts()
    hist_data['regplot']=max(hist_data['Close'])*(2+hist_data['regime'])/8 
    
    hist_data['regplot'].plot(title= name,  grid=False,lw=1.5)
    #plt.ylim([-1.1, 1.1])
    
    '''Market / Strategy comparison '''
    
    hist_data['market'] = np.log(hist_data['Close'] / hist_data['Close'].shift(1))
    hist_data['strategy'] =  hist_data['market'] *(1+hist_data['regime'].shift(1))
    
    hist_data[['market','strategy']].cumsum().apply(np.exp).plot(title=name,grid=False, figsize=(8, 5))
    
    X=hist_data['strategy'].cumsum().iloc[-1]-hist_data['market'].cumsum().iloc[-1]
    
    print('final data pt. difference b/t market & strat: ',X)
#    return X

qtech()





