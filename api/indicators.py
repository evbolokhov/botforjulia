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


def moving_avg(x):
    return sum(x) / len(x)


def moving_std(x, avg):
    return (sum((a - avg) ** 2 for a in x) / len(x)) ** 0.5


def bollinger_breakout_strategy(closes, window_size, n_std):
    avgs = []  # список значений среднего
    stds = []  # список значений стандартного отклонения
    for i in range(len(closes)):
        if i <= window_size - 1:
            avgs.append(None)
            stds.append(None)
        else:
            avg = moving_avg(closes[i - window_size:i])
            std = moving_std(closes[i - window_size:i], avg)
            avgs.append(avg)
            stds.append(std)

    upper_band = []
    lower_band = []
    for i in range(len(avgs)):
        if avgs[i] is not None and stds[i] is not None:
            upper_band.append(avgs[i] + n_std * stds[i])
            lower_band.append(avgs[i] - n_std * stds[i])
        else:
            upper_band.append(None)
            lower_band.append(None)

    positions = [0] * len(closes)
    for i in range(window_size - 1, len(closes)):
        if upper_band[i] is not None and closes[i] > upper_band[i]:
            positions[i] = 1
        elif lower_band[i] is not None and closes[i] < lower_band[i]:
            positions[i] = -1

    return positions, upper_band, lower_band
