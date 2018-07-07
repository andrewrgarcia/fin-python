# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 00:27:07 2018

@author: garci
"""

'''
Geometric Brownian Motion (GBM) algorithm for stock prediction

trading days:
annual drift (mu) and volatility (sig)
initial equity price (S0)
trading period, days (tT)
'''

import random
import numpy as np
import matplotlib.pyplot as plt


def start(Npop=20,mua=0.015,siga=0.015,S0=45.03, tT=220 ):
    
    def stockpred(mua,siga,S0,tT):
        n=1

        
        'daily:'
        mud=mua*tT**(-1)
        sigd=siga*tT**(-0.5)
        'drift(return)'
        retd=mud-0.5*sigd**(2)
        
        'Wiener process'
        wT=random.gauss(0,1)
        
        logret=n*(retd+sigd*wT)

        S=S0*np.exp(logret)
        
        y=[]
        for i in range(0,tT):
            wT=random.gauss(0,1)
            logret=n*(retd+sigd*wT)
            S=S*np.exp(logret)
            y.append(S)
        
        plt.plot(y)
          
    N=0  
    while N < Npop:
        stockpred(mua,siga,S0,tT)
        N+=1
    
    plt.ylabel('X Price')
    plt.xlabel('Future trading days (alternative paths)')
    plt.show()
    
start()