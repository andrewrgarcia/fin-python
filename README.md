# Quantitative finance with python
#### Andrew Garcia, 2019

Published code _**backtest_simple.py**_ is an **ADAPTED** script from the codes from _**Python for Finance (Yves Hilpisch, 2014)**_ which show simple technical analysis algorithms for stocks. Now integrated with cryptocurrencies-importing capabilities from Binance (_**binancereader.py**_)

![Screenshot](Figure_1.png)

Historical Data

![Screenshot](Figure_2.png)

Strategy results (Buy-sell-hold regime in red)

![Screenshot](Figure_3.png)

Market v. Strategy

![Screenshot](Figure_4.png)

Rel. return per run

The figures showed here are the results of an optimization script _**blackswanclimb.py**_ which integrates _**backtest_simple.py**_ to a [secret] Monte Carlo algorithm (not pushed here; confidential) which finds optimal backtesting parameters for a certain stock, showing optimal **"BUY/HOLD/SELL"** regimes (step-wise red line in 2nd plot) for a certain trading window.


<img src="black_swan.jpg" alt="drawing" width="350"/>

**It's a black swan!**
