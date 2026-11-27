"""
In general we do not want to prolong these indicators (make them persistent meaning the signal occurs
and then we keep it on even after the signal ends). The idea is that these are closes depending on
the prev ohlc. This is different than the say the BB squeeze which occurs much less (6 month low) and
so when these occur we may want to prolong the signal. Especially since this could be one day. Could
be interesting to look if longer the squeeze the more explosive.
"""

import pandas as pd
import numpy as np

def bull_flip( close):
    s = pd.Series(close)
    return ((s.shift(1) < s.shift(5)) & (s > s.shift(4))).astype(float).values

def bear_flip(close):
    s = pd.Series(close)
    return ((s.shift(1) > s.shift(5)) & (s < s.shift(4))).astype(float).values

def buytd_set(close):
    s = pd.Series(close)
    condition = s < s.shift(4)

    count = 0
    result = []

    for cond in condition:
        if cond:
            count += 1
        else:
            count = 1 #TODO: why is the count 1 and not zero if the streak is broken
        result.append(count)

    return np.array(result)

def selltd_set(close):
    s = pd.Series(close)
    condition = s > s.shift(4)

    count = 0
    result = []

    for cond in condition:
        if cond:
            count += 1
        else:
            count = 1 #TODO: why is the count 1 and not zero if the streak is broken
        result.append(count)

    return np.array(result)

if __name__ == "__main__":
    from backtesting.test import GOOG
    GOOG['BearTD_Flip'] = bear_flip(GOOG['Close'])
    GOOG['BullTD_Flip'] = bull_flip(GOOG['Close'])
    GOOG['BuyTD_Set'] = buytd_set(GOOG['Close'])
    GOOG['SellTD_Set'] = selltd_set(GOOG['Close'])