from sma_strategy import compare_two_sma
import pandas as pd

#create sweep range for multiple opportunities
#short window: 5 to 50, by 5
#long window: 10 to 200, by 10

#compare_two_sma(stock, start,end, a: int, b: int)

def sma_sweep(stock, start, end):

    #Dataframe can be used for heatmap later
    df = pd.DataFrame() 

    #Only compute index value once
    indexed_value, _ = compare_two_sma(stock, start, end, 1, 2)

    for i in range(5,50,5):
        for j in range(10,200,10):

            if i != j and j > i:

                _, trading_value = compare_two_sma(stock, start, end, i, j)

                df.loc[i, j] = trading_value

    print(df)



#sma_sweep('IVV.AX','2020-01-01', '2026-01-01')