from yfin_livedata import get_underlying_stock_list, get_stock_data
from sma_algo import sma_faster

# Strategy: buy when smaller date parameter sma crosses larger sma upwards, sell when smaller date parameter sma crosses larger one downwards

def get_sma_list(stock, start, end, lookback_period: int):

    close_values, date_values, raw_vals = get_underlying_stock_list(stock, start, end)

    return sma_faster(close_values, lookback_period)

def compare_two_sma(stock, start,end, a: int, b: int):

    #setting variables for loop & terminal messages
    if a < b:
         temp = b
         b = a
         a = temp
    if a == b:
         raise ValueError

    indicator_1 = get_sma_list(stock, start, end, a)
    indicator_2 = get_sma_list(stock, start, end, b)
    
    close_values, date, _ = get_underlying_stock_list(stock, start, end)

    trading_balance = 0
    indexed_balance = close_values[-1] - close_values[0]

    date_last_bought_idx = 0
    date_last_sold_idx = 0

    for i in range(len(indicator_2)):

        if i == 0:               
            continue            # 'continue' prevents negative indexing as opposed to pass

        if indicator_2[i] != None and indicator_2[i-1] != None and indicator_1[i] != None and indicator_1[i-1] != None:

            curr_date = date[i]
            curr_underlying = close_values[i]

            #Conditions for a buy/sell
            sell_prereq = indicator_2[i-1] > indicator_1[i-1] and indicator_2[i] < indicator_1[i] and date_last_bought_idx > date_last_sold_idx   #smaller day crosses below larger day, date last bought is > date last sold
            buy_prereq = indicator_2[i-1] < indicator_1[i-1] and indicator_2[i] > indicator_1[i] #smaller day crosses above larger day
            final_day = curr_date == date[-1]

            #on the last day we have to sell to see return
            if final_day:
                if date_last_bought_idx > date_last_sold_idx:
                    print(f"FINAL SELL at {curr_date}: Close value of underlying stock: {curr_underlying}")
                    p2p_return = curr_underlying - close_values[date_last_bought_idx]
                    print(f"The point to point return since the last buy is {p2p_return} point/s\n")
                    trading_balance += p2p_return

            #buy
            elif buy_prereq:
                    print(f"BUY at {curr_date}: The {b} day SMA has crossed ABOVE the {a} Day SMA \nClose value of underlying stock: {curr_underlying}\n")
                    date_last_bought_idx = i

            #sell
            elif sell_prereq:
                    print(f"SELL at {curr_date}: The {b} day SMA has crossed BELOW the {a} Day SMA \nClose value of underlying stock: {curr_underlying}")
                    p2p_return = curr_underlying - close_values[date_last_bought_idx]
                    trading_balance += p2p_return
                    print(f"The point to point return since the last buy is {p2p_return} point/s\n")
                    date_last_sold_idx = i


    print(f"The indexed return is {indexed_balance} point/s and the trading return is {trading_balance} point/s")
              

# start_date = "2025-01-01"
# end_date = "2026-08-24"        
# compare_two_sma(start_date, end_date, 5, 30)