from sma_strategy import compare_two_sma
from datetime import datetime

def gui():
    stock = stock_choice()
    start, end = date_request()
    strategy_choice(stock, start, end)

def stock_choice():

    return str(input("Input the Yahoo Finance Ticker for the stock you wish to analyse: "))

def strategy_choice(stock, start_date, end_date):
    strat_choice = int(input("Which strategy would you like to backtest?" \
              "\n\nSelect the strategy by typing in the number and pressing Enter\n"
    "\n1. Simple Moving Average\n   \
    \n"))

    if strat_choice == 1:
        print("\nSimple Moving Average (SMA) chosen, requiring two (2) lookback periods\n")

        while True:
            try:
                a = int(input("Length of first moving average (in days): "))
                b = int(input("Length of second moving average (in days): "))

                if a != b:
                    break
                elif a == b:
                    print("\nTo compare simple moving averages, lookback periods cannot be identical, try again\n")
            except ValueError:
                print("Enter a valid number, try again\n")

        print("\n")

        compare_two_sma(stock, start_date, end_date, a, b)


def date_request():
    print("\nChoose a period for analysis, dates must be entered with the following syntax: YYYY-MM-DD\n")

    while True:
        try:
            start = datetime.strptime(input("Start date: "), "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid format, try again\n")

    while True:
            try:
                end = datetime.strptime(input("End date: "), "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid format, try again\n")
        
    #start = str(input("Start date: "))
    #end = str(input("End date: "))

    return start, end


gui()