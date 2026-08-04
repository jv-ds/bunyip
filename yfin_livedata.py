import yfinance as yf
import json

from sma import sma_naive, sma_faster

import plotly.express as px

def get_ivv(start, end):
    stock = yf.Ticker("IVV.AX")

    data = {}

    close_history = stock.history(start=start, end=end)['Close']
    len_prices = len(close_history)

    for i in range(len_prices):
        idx = close_history.index[i]
        val = float(close_history.values[i])

        data[idx] = val

    # .index for date, .values for price
    
    return(data)

#get_ivv()
full_list = get_ivv("2026-01-01","2026-08-03")
#thirty_day = sma_faster(get_ivv(),30)
#five_day = sma_faster(get_ivv("2026-01-01","2026-08-03"),5)


print(full_list)

print(get_ivv("2026-01-01","2026-08-03").keys())
print(get_ivv("2026-01-01","2026-08-03").values())
