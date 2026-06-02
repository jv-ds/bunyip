## So what actually is a trading strategy?

From first principles, a trading strategy is a set of rules which answers one fundamental question: "should I buy, hold or sell this thing?".

More complicated strategies answer "how much" and "when" (long/shorting).

This set of rules turns data (price, figures from reports etc) into signals. A signal is just a hunch on what will happen next.

This signal will turn into a position (an actual financial decision).

Thus, in real terms for my use case, a trading strategy is a set of instructions which can be executed by a computer, it is a sequence of if/else statements.

Referring to Ernest Chan's book, 'Algorithmic Trading', there are two basic strategies:

1. Momentum
   "Things that go up tend to keep going up"
2. Mean reversion
   "Things that are too far from the average tend to go back to average"

These two patterns occur simultaneously in markets for different products, at different times. For example, one company might rally for 1-2 years (momentum), but then eventually correct/drawdown over the course of 5-10 years (mean reversion).

## Simple Moving Average (SMA)

The simplest strategy utilising the mean reversion strategy is the simple moving average (SMA).

This is simply the average of the last n values for a financial product.

```
prices = [11,12,13,14,17] 
sum = sum(prices)
n = len(prices) + 1

sma = sum/n
```

The whole point of this strategy is that it shows the underlying pattern, rather than the day to day fluctuations.

As n rises, so does the robustness of the mean. But the tradeoff is the lag- it reflects the trend after the inflection points of interest have already happened.

The classic use of this strategy is to identify the crossover point, when the fast SMA crosses the slow SMA.

When fastSMA crosses above slowSMA, this is read as a bullish trend confirmation and the inverse as bearish.
