def sma_naive(prices: list, n: int):
    #prices = list of prices chronologically ordered
    #n = number of days to go back (window length)

    moving_avg = []

    for i in range(len(prices)):
        if (i+1) >= n:
            temp_total = 0
            for j in range(n):
                temp_total += prices[i-j]
            moving_avg.append(temp_total/n)
        elif (i+1) < n:
            moving_avg.append(None)

    return moving_avg


dummy = [1,2,3]
days_interested = 0


print(f"The simple moving average is: {sma_naive(dummy,days_interested)}")