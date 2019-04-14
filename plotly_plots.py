# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 13:09:36 2019

@author: garci
"""

from plotly_cred import info

import plotly
plotly.tools.set_credentials_file(username=info()[0], api_key=info()[1])
import plotly.plotly as py
import plotly.graph_objs as go

def plyfin(hist_data,ticker_name,roll_mean1,roll_mean2,crypto):


    'PLOT # 1: Stock Price, Moving Averages and Buy-Sell Regimes'
    
    if crypto == False:
    
        trace = go.Ohlc(x=hist_data.index,
                        open=hist_data['open'],
                        high=hist_data['high'],
                        low=hist_data['low'],
                        close=hist_data['close'],
                        name = 'candlesticks')
        
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
    
    layout=go.Layout(title=ticker_name+' Coin' if crypto == True \
                     else ticker_name+' Stock', xaxis={'title':'Date'}, yaxis={'title':''}) 
    
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename=ticker_name+' Coin' if crypto == True else ticker_name+' Stock')
    
    
    'PLOT # 2: Backtesting Strategy Assessment'
    trce1 = go.Scatter(x=hist_data.index,
                       y=hist_data['market'],
                       name ='market value')
    trce2 = go.Scatter(x=hist_data.index,
                       y=hist_data['strategy'],
                       name ='strategy value')
    
    data= [trce1,trce2]
    layout=go.Layout(title=ticker_name+' Coin Strategy Assessment' if crypto == True \
                     else ticker_name+' Stock Strategy Assessment', xaxis={'title':'Date'}, yaxis={'title':''})
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename=ticker_name+' Coin Strategy Assessment' if crypto == True \
                     else ticker_name+' Stock Strategy Assessment')
    
    print('Confirmation: plots sent to plot.ly SUCCESSFUL')
