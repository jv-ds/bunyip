from yfin_livedata import get_underlying_stock_list, get_5d_sma_list, get_30d_sma_list

# Strategy: buy when 5d sma crosses 30d sma upwards, sell when 5d sma crosses 30d downwards

def thirty_vs_five(start,end):
    thirty_d = get_30d_sma_list(start, end)
    five_d = get_5d_sma_list(start, end)
    close_values, date, _ = get_underlying_stock_list(start, end)

    trading_balance = 0
    indexed_balance = close_values[-1] - close_values[0]

    date_last_bought_idx = 0
    date_last_sold_idx = 0

    for i in range(len(five_d)):

        if i == 0:               
            continue            # 'continue' prevents negative indexing as opposed to pass

        if five_d[i] != None and five_d[i-1] != None and thirty_d[i] != None and thirty_d[i-1] != None:

            curr_date = date[i]
            curr_underlying = close_values[i]

            #Conditions for a buy/sell
            sell_prereq = five_d[i-1] > thirty_d[i-1] and five_d[i] < thirty_d[i] and date_last_bought_idx > date_last_sold_idx   #5 day crosses below 30 day, date last bought is > date last sold
            buy_prereq = five_d[i-1] < thirty_d[i-1] and five_d[i] > thirty_d[i] #5 day crosses above 30 day
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
                    print(f"BUY at {curr_date}: The 5 day SMA has crossed ABOVE the 30 Day SMA \nClose value of underlying stock: {curr_underlying}\n")
                    date_last_bought_idx = i

            #sell
            elif sell_prereq:
                    print(f"SELL at {curr_date}: The 5 day SMA has crossed BELOW the 30 Day SMA \nClose value of underlying stock: {curr_underlying}")
                    p2p_return = curr_underlying - close_values[date_last_bought_idx]
                    trading_balance += p2p_return
                    print(f"The point to point return since the last buy is {p2p_return} point/s\n")
                    date_last_sold_idx = i


    print(f"The indexed return is {indexed_balance} point/s and the trading return is {trading_balance} point/s")
              

start_date = "2025-01-01"
end_date = "2026-08-24"        
thirty_vs_five(start_date, end_date)