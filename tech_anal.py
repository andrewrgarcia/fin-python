# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 11:54:40 2018

@author: garci
"""

import numpy as np
import pandas as pd
#import pandas.io.data as web
#from pandas_datareader import data, wb

import stock_params
'''stock_params.py: returns ticker name (as a string), 
rolling means 1 and 2 and SD (as numbers) from vector def
i.e. def Netflix:
        return ['name', roll_mean1,roll_mean2, SD]
will not push this script; personal stock info'''


def qtech():
    
    name, roll_mean1,roll_mean2, SD = stock_params.Dominos()

    hist_data = pd.read_csv(name+'.csv')
    hist_data.info()
    hist_data[['date','close']].plot(title = name, x='date', grid=True, figsize=(8, 5))
    
   
    ''' Historical data with moving averages '''
    
    hist_data[str(roll_mean1)+'d'] = np.round(pd.rolling_mean(hist_data['close'], window=roll_mean1), 2)
    hist_data[str(roll_mean2)+'d'] = np.round(pd.rolling_mean(hist_data['close'], window=roll_mean2), 2)
    
    hist_data[['close', str(roll_mean1)+'d', str(roll_mean2)+'d']].tail
    
    hist_data[['date','close', str(roll_mean1)+'d', str(roll_mean2)+'d']].plot(x='date',grid=True, figsize=(8, 5))
    
    
    '''regime det. '''
    
    hist_data['42-252'] = hist_data[str(roll_mean1)+'d'] - hist_data[str(roll_mean2)+'d']
    
    hist_data['42-252'].tail
    
    hist_data['regime'] = np.where(hist_data['42-252'] > SD, 1, 0)
    hist_data['regime'] = np.where(hist_data['42-252'] < -SD, -1, hist_data['regime'])
    hist_data['regime'].value_counts()
    
    hist_data['regime'].plot(title= name,  grid=True,lw=1.5)
    #plt.ylim([-1.1, 1.1])
    
    '''Market / Strategy comparison '''
    
    hist_data['market'] = np.log(hist_data['close'] / hist_data['close'].shift(1))
    hist_data['strategy'] =  hist_data['market'] *(1+hist_data['regime'].shift(1))
    
    hist_data[['market','strategy']].cumsum().apply(np.exp).plot(title=name,grid=False, figsize=(8, 5))
    
    X=hist_data['strategy'].cumsum().iloc[-1]-hist_data['market'].cumsum().iloc[-1]
    
    print('final data pt. difference b/t market & strat: ',X)

qtech()




