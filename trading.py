# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 01:36:54 2019

@author: garci
"""
from trade_auth import keys
from binance.client import Client
from cerberus33 import *
'''trading bot - developing stages
Andrew'''

api_key, api_secret = keys()
client = Client(api_key, api_secret)

# get market depth
depth = client.get_order_book(symbol='BNBBTC')


portfolio=['THETA','BNB']
buy, sell = screening(portfolio,50,crypto='y')
assetbal = []
#for i in portfolio:
#    assetbal.append(client.get_asset_balance(asset=i))
assetbal = [200,100]
for S in sell:
    order = client.create_test_order(
        symbol= S +'BTC',
        side=Client.SIDE_SELL,
        type=Client.ORDER_TYPE_MARKET,
        quantity=float(assetbal[portfolio.index(S)]))
    print(assetbal[portfolio.index(S)])
    
for B in buy:
    # place a test market buy order, to place an actual order use the create_order function
    order = client.create_test_order(
        symbol= B + 'BTC',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=float(assetbal[portfolio.index(B)]))
    print(assetbal[portfolio.index(B)])
    
print(client.get_account())

print()
print(client.get_account_status())

#print(client.get_asset_details())