# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 01:36:54 2019

@author: garci
"""
from trade_auth import keys
from binance.client import Client
from cerberus33 import *
'''trading interface: developing stages
Andrew'''

api_key, api_secret = keys()
client = Client(api_key, api_secret)

# get market depth
depth = client.get_order_book(symbol='BNBBTC')


portfolio=['THETA','BNB','ETH']
#buy, sell = screening(portfolio,50,crypto='y')
assetbal =  []
[assetbal.append(client.get_asset_balance(asset=i)) for i in portfolio]
print(assetbal)

print('test start: \n')
buy, sell = ['THETA','BNB'], ['ETH']
assetbal = [200,100,500]

'Sell: all bought coins in sell regime sold'
qsell_total = 0
for S in sell:
    qsell = assetbal[portfolio.index(S)]
    order = client.create_test_order(
        symbol= S +'BTC',
        side=Client.SIDE_SELL,
        type=Client.ORDER_TYPE_MARKET,
        quantity=qsell)
    
    qsell_total += qsell
    print(S + 'BTC')
    print(0)
    print('(-{})'.format(qsell))
    print(client.get_all_orders(symbol= S + 'BTC'))
'Buy: allocate funds from total profits evenly'
for B in buy:
    qbuy = qsell_total / len(buy)
    # place a test market buy order, to place an actual order use the create_order function
    order = client.create_test_order(
        symbol= B + 'BTC',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=qbuy)
    print(B + 'BTC')
    print(assetbal[portfolio.index(B)]+qbuy)
    print('(+{})'.format(qbuy))
    print(client.get_all_orders(symbol=B + 'BTC'))

#print(client.get_account())

#print()
#print(client.get_account_status())

#print(client.get_asset_details())

