from yfin_livedata import get_underlying_stock_list, get_5d_sma_list, get_30d_sma_list

# Strategy: buy when 5d sma crosses 30d sma upwards, sell when 5d sma crosses 30d downwards

def thirty_vs_five(start,end):
    thirty_d = get_30d_sma_list(start, end)

    five_d = get_5d_sma_list(start, end)

    close_values, date, _ = get_underlying_stock_list(start, end)

    start_underlying = close_values[0]
    end_underlying = close_values[-1]

    trading_balance = 0
    indexed_balance = end_underlying - start_underlying

    date_last_bought_idx = 0
    date_last_sold_idx = 0

    for i in range(len(five_d)):
        if five_d[i] != None and five_d[i-1] != None and thirty_d[i] != None and thirty_d[i-1] != None:

            curr_date = date[i]
            curr_underlying = close_values[i]

            #on the last day we have to sell to see return
            if curr_date == date[-1]:
                print("diddiaujhgfialkhsfakljhsfgkjhasd")
                if date_last_bought_idx > date_last_sold_idx:
                    print(f"FINAL SELL {curr_date}: Close value of underlying stock: {curr_underlying}")
                    #sell
                    p2p_return = curr_underlying - close_values[date_last_bought_idx]
                    print(f"The point to point return is{p2p_return}\n")
                    trading_balance += p2p_return

            #buy
            elif five_d[i-1] < thirty_d[i-1]:
                if five_d[i] > thirty_d[i]:
                    #5 day crosses above 30 day
                    print(f"BUY on {curr_date}: The 5 day SMA has crossed ABOVE the 30 Day SMA \nClose value of underlying stock: {curr_underlying}\n")
                    #buy
                    date_last_bought_idx = i

            #sell
            elif five_d[i-1] > thirty_d[i-1]:
                if five_d[i] < thirty_d[i]:
                    #5 day crosses below 30 day
                    print(f"SELL {curr_date}: The 5 day SMA has crossed BELOW the 30 Day SMA \nClose value of underlying stock: {curr_underlying}")
                    print(f"The stock was las bought at {close_values[date_last_bought_idx]}")
                    #sell
                    p2p_return = curr_underlying - close_values[date_last_bought_idx]
                    trading_balance += p2p_return
                    print(f"The point to point return is{p2p_return}\n")
                    date_last_sold_idx = i


    print(f"The indexed return is {indexed_balance} and the trading return is {trading_balance}")
              

start_date = "2026-01-01"
end_date = "2026-08-24"        
print(thirty_vs_five(start_date, end_date))