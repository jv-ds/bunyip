import yfinance as yf

def get_stock_data(stock, start, end):
    stock = yf.Ticker(stock)

    data = {}

    close_history = stock.history(start=start, end=end)['Close']
    len_prices = len(close_history)

    for i in range(len_prices):
        idx = close_history.index[i]
        val = float(close_history.values[i])

        data[idx] = val

    # .index for date, .values for price

    #.items retrieves index values
    #.values retrieves value values
    
    return(data)


def get_underlying_stock_list(stock, start, end):

    stock_list = {}

    raw_vals = get_stock_data(stock, start, end)

    point_of_interest = list(raw_vals.items())
    #Each item is tuple: (date + time, price value)

    for p in point_of_interest:

        timestamp_item = p[0]
        date_value = timestamp_item.date()

        close_value = p[1]

        stock_list[f"{date_value}"] = close_value       #each idx in dict contains date: close value at that date
        
    close_values = list(stock_list.values())
    date_values = list(stock_list.keys())


    return close_values, date_values, raw_vals    



# print(get_5d_sma_list(start_date, end_date))