import pandas as pd

def percent_b(price, window=20, width=2.0):
    mid = price.rolling(window).mean()
    std = price.rolling(window).std(ddof=0)
    lower = (mid - width * std).values
    higher = (mid + width * std).values
    return ((price-lower)/(higher-lower)).values


def bb_lower(price, window=20, width=2.0):
    mid = price.rolling(window).mean()
    std = price.rolling(window).std(ddof=0)
    return (mid - width * std).values


def bb_higher(price, window=20, width=2.0):
    mid = price.rolling(window).mean()
    std = price.rolling(window).std(ddof=0)
    return (mid + width * std).values


def bb_squeeze(price, window=20, width=2.0, squeeze_window=20):
    """
    was 120 for the daily
    """
    mid = price.rolling(window).mean()
    std = price.rolling(window).std(ddof=0)
    bw = (2 * width * std) / mid  # equivalent to (upper - lower) / mid
    return (bw == bw.rolling(squeeze_window).min()).astype(float).values

def bandwidth(price, window=20, width=2.0, squeeze_window=20):
    mid = price.rolling(window).mean()
    std = price.rolling(window).std(ddof=0)
    bw = (2 * width * std) / mid  # equivalent to (upper - lower) / mid
    return bw.values


def rsi(close, window=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    rs = avg_gain / avg_loss
    return (100 - 100 / (1 + rs)).values


def mfi(high, low, close, volume, window=14):
    typical = pd.Series((high + low + close) / 3)  # Could look at including the open
    rmf = typical * volume # Raw Money flow
    pos_flow = rmf.where(typical > typical.shift(1), 0.0) # if the current typical is higher than one day previous
    neg_flow = rmf.where(typical < typical.shift(1), 0.0) # else
    pmf = pos_flow.rolling(window).sum()
    nmf = neg_flow.rolling(window).sum()
    mfr = pmf / nmf
    return (100 - 100 / (1 + mfr)).values

if __name__ == "__main__":
    from backtesting.test import GOOG
    import matplotlib.pyplot as plt
    # add in the BBands stuff
    # 1) make a new column for the price, called the typical price
    # Open + High+Low+close /4
    GOOG['Typical_Price'] = (GOOG['Open'] + GOOG['High'] + GOOG['Low'] + GOOG['Close']) / 4
    # 3) bollinger band calculation 20 day SMA with std 2 be sure to use 1/n for std calculation not 1/(n-1)
    # slightly wider bands. Using the typical price but this could be better with close we need to do tests.
    GOOG['BB_Mid'] = GOOG['Typical_Price'].rolling(window=20).mean()
    bb_std = GOOG['Typical_Price'].rolling(window=20).std(ddof=0)  # population std (1/n)
    GOOG['BB_Upper'] = GOOG['BB_Mid'] + 2 * bb_std
    GOOG['BB_Lower'] = GOOG['BB_Mid'] - 2 * bb_std

    # 4) %b = Last-lower BB / (upper BB-lower BB)
    GOOG['BB_Pct_B'] = (GOOG['Typical_Price'] - GOOG['BB_Lower']) / (GOOG['BB_Upper'] - GOOG['BB_Lower'])

    # 5) bw = (upper BB - lower BB) / middle BB
    GOOG['BB_BW'] = (GOOG['BB_Upper'] - GOOG['BB_Lower']) / GOOG['BB_Mid']

    # 6 month low squeeze signal (~120 trading days)
    GOOG['BB_Squeeze'] = GOOG['BB_BW'] == GOOG['BB_BW'].rolling(window=120).min()

    ###### Explore stats part
    num_days = 7
    GOOG['future_return'] = GOOG['Close'].shift(-num_days) / GOOG['Close'] - 1

    # triggered = GOOG[(GOOG['BullTD_Flip'] == 1) & (GOOG['BB_Squeeze'] == True)]
    triggered = GOOG[(GOOG['BB_Squeeze'] == True)]
    print(f"BullTD_Flip + BB_Squeeze occurred {len(triggered)} times")
    print(f"Avg return {num_days} days later: {triggered['future_return'].mean():.2%}")
    print(f"Win rate: {(triggered['future_return'] > 0).mean():.2%}")

    triggered['future_return'].hist(bins=10, edgecolor='k')
    plt.axvline(triggered['future_return'].median(), color='orange', linestyle='--', label='Median')
    plt.axvline(triggered['future_return'].mean(), color='blue', linestyle='--', label='Mean')
    plt.title(f"{num_days}-Day Return Distribution After condition")
    plt.xlabel("Return")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()