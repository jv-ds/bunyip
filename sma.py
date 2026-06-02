def sma(prices: list, n: int):
    #prices = list of prices chronologically ordered
    #n = number of days to go back

    total = 0
    moving_avg = []

    for i in range(n):
        total += prices[-i-1]
        moving_avg.append(total/(i+1))


    return moving_avg


dummy = [1,2,3,4,5,6,7,8,9,10]
days_interested = 10


print(f"The simple moving average is: {sma(dummy,days_interested)}")