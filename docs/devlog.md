# Development Log



## 28 Aug 2026

#### Core Backtester logic done

Built dual SMA crossover strategy:

* Buys when shorter SMA crosses above longer SMA, sells when it crosses below
* Forced sell on final day to compare against buying and holding

Cleaned up functions, logic & parameterised input for stock and the SMA lookback periods. 

Created simple terminal GUI for user. 


Next step: Create a parameter sweep i.e. compare multiple SMA strategies simultaneously
