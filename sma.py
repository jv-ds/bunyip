def sma_naive(prices: list, n: int):
    #prices = list of prices chronologically ordered
    #n = number of days to go back (window length)

    if n <= 0:
        raise ValueError("Window must be larger than 0")

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

def sma_faster(prices: list, n: int):
    moving_avg = []

    ongoing_sum = 0

    for i in range(n):
        ongoing_sum += prices[i]

    for i in range(len(prices)):
        if i < n-1:
            moving_avg.append(None)
        elif i == n-1:
            moving_avg.append((ongoing_sum/n))
        elif i > n-1:
            ongoing_sum -= prices[i-n]

            ongoing_sum += prices[i]

            moving_avg.append((ongoing_sum/n))
    
    return moving_avg

        

if __name__ == "__main__":
    dummy = [1,2,3,4,5,6,7,8,9,10]
    days_interested = 3


    print(f"The simple moving average is: {sma_faster(dummy,days_interested)}")