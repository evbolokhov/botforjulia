import numpy as np


def ema(data, period):
    ema_values = np.zeros_like(data)
    sma = np.mean(data[:period])
    ema_values[period - 1] = sma
    multiplier = 2 / (period + 1)

    for i in range(period, len(data)):
        ema_values[i] = (data[i] - ema_values[i - 1]) * multiplier + ema_values[i - 1]

    return ema_values


def rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi
