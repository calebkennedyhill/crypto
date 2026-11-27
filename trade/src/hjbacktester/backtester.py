import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import DeMark as DM
from backtesting import Backtest, Strategy
import Bollinger as BB


def _vol_stan_panel(vol, ma_window=20):
    """Returns [vol_MA, reference_100] as a 2D array for a volume subplot panel.
    vol_stan is already the standardized volume (V / MA_50 * 100).

        data['RawVolume'] = data['Volume']
    vol_ma50 = data['RawVolume'].rolling(window=50).mean()
    data['Volume'] = data['RawVolume'] / vol_ma50 * 100
    """
    vol_series = pd.Series(vol)
    vol_ma = vol_series.rolling(window=ma_window).mean().values

    vol_stan = vol_series/vol_ma * 100
    ref_100 = np.full(len(vol_stan), 100.0)
    return np.vstack([vol_stan, ref_100])


def _mfi_panel(high, low, close, volume, band_width):
    """Returns MFI + its BB lower/upper as a 2D array for a single subplot panel."""
    mfi = BB.mfi(high, low, close, volume, window=10)
    mfi_s = pd.Series(mfi)
    return np.vstack(
        [mfi, BB.bb_lower(mfi_s, window=40, width=band_width), BB.bb_higher(mfi_s, window=40, width=band_width)])


class DeMarkBBStrategy(Strategy):
    pb_buy = 0.6
    # pb_buy = 0.8
    # pb_sell = 0.1
    pb_sell = 0.2
    # mfi_pb_buy = 0.3
    mfi_pb_buy = 0.8
    # mfi_pb_sell = 0.0
    mfi_pb_sell = 0.2

    def init(self):
        # Data prep
        o, h, l, c = self.data.Open, self.data.High, self.data.Low, self.data.Close
        # mfi_band_width = 1.8  # most stocks around 88% this is good, visually confirmed not quantatively.
        mfi_band_width = 1.6  # most stocks around 88% this is good, visually confirmed not quantatively.

        vol = pd.Series(self.data.Volume)   # raw volume for MFI
        # vol_stan = pd.Series(self.data.Volume)  # standardized volume (V / MA_50 * 100)
        self._tp = pd.Series((o + h + l + c) / 4)  # typical price

        # indicators and others. order matters! need to update post bokeh when adding removing.
        self.vol_panel = self.I(_vol_stan_panel, vol,
                                overlay=False, name='Stan Vol',
                                color=['black' ,'red'])

        # self.bull_flip = self.I(DM.bull_flip, c, plot=False)
        self.bull_flip = self.I(DM.bull_flip, c, )
        # TODO: add in 20 day SMA for the middle of the BB band
        self.bb_lower_ind = self.I(BB.bb_lower, self._tp)
        self.bb_higher_ind = self.I(BB.bb_higher, self._tp)
        #TODO: I dont think we need the persistent any more can just index

        # self.bb_squeeze = self.I(BB.bb_squeeze_persistent, self._tp)
        self.bb_squeeze = self.I(BB.bb_squeeze, self._tp)
        self.pb = self.I(BB.percent_b, self._tp)
        self.rsi = self.I(BB.rsi,self._tp)
        self.bandwidth = self.I(BB.bandwidth,self._tp )
        self.mfi_panel = self.I(_mfi_panel, h, l, c, vol, mfi_band_width,
                                overlay=False, name='MFI',
                                color=['blue', 'orange', 'orange'])
        self.mfi_pb = self.I(BB.percent_b, pd.Series(self.mfi_panel[0]), window=40, width=mfi_band_width)



    def next(self):
        """
        for persistent use for example self.bb_squeeze[-20:].any()
        """
        # if self.bull_flip[-1] and (self.bb_squeeze[-1] or (self.pb[-1] > self.pb_buy and self.mfi_pb[-1] >self.mfi_pb_buy)):
        # if self.bull_flip[-1] and (self.bb_squeeze[-20:].any() or (self.pb[-1] > self.pb_buy and self.mfi_pb[-1] >self.mfi_pb_buy)):
        # if self.bull_flip[-1] and (self.bb_squeeze[-20:] and (self.pb[-1] > self.pb_buy and self.mfi_pb[-1] >self.mfi_pb_buy)):
        # if self.bull_flip[-1] and (self.bb_squeeze[-1] and self.mfi_pb[-1] >self.mfi_pb_buy):
        # if self.bull_flip[-1] and (self.pb[-1] > self.pb_buy and self.mfi_pb[-1] >self.mfi_pb_buy):
        # if self.pb[-1] > self.pb_buy and self.mfi_pb[-1] >self.mfi_pb_buy:
        # if (self.bb_squeeze[-1] or self.pb[-1] > self.pb_buy) and self.mfi_pb[-1] >self.mfi_pb_buy:
        # if (self.bb_squeeze[-20:-2].any() and self.pb[-1] > self.pb_buy) and self.mfi_pb[-1] >self.mfi_pb_buy:
        # if self.bb_squeeze[-1] and self.mfi_pb[-1] >self.mfi_pb_buy:
        # if self.bb_squeeze[-20:].any() and self.mfi_pb[-1] >self.mfi_pb_buy:
        if self.bb_squeeze[-20:].any() and self.mfi_pb[-1] >self.mfi_pb_buy and (self.bandwidth[-1]> self.bandwidth[-2] >self.bandwidth[-3]):
        # if self.bull_flip[-1] and self.bb_squeeze[-1]:
        # if self.bb_squeeze[-1]:
            if not self.position:
                self.buy()
        ################################ Sequence
        # if self.bb_squeeze[-1]:
        #     if self.pb[-1]> 1.0:
        #         if self.pb[-1] > self.pb_buy and self.mfi_pb[-1] >self.mfi_pb_buy:
        #
        #             if not self.position:
        #                 self.buy()
                # self.buy(sl=self.data.Close[-1] * 0.95)
            # This code handles the case when we have a position and then a second buy signal occurs and
            # then we sell and rebuy. There are other options here such as pyriamd into the position.
            # test which one is best.
            # if self.position:
            #     self.position.close()
            #     self.buy()
        # Exit: lower BB declined from prior bar (bands expanding downward)
        # if self.position and self.bb_lower_ind[-1] < self.bb_lower_ind[-2] and self.bb_lower_ind[-1] < self.bb_lower_ind[-3] and self.bb_lower_ind[-1] < self.bb_lower_ind[-5] :
        # if self.position and self.pb[-1] < 0.0 and self.pb[-2] < 0.0:
        # if self.position and self.pb[-1] < 0.05 and self.pb[-2] < 0.05:
        # if self.position and self.pb[-1] < 0.5 and self.pb[-2] < 0.5 and self.pb[-3] < 0.5:
        if self.position and self.pb[-1] < self.pb_sell and self.mfi_pb[-1] < self.mfi_pb_sell:
            self.position.close()


def optim_explore(bt):
    from backtesting.lib import plot_heatmaps
    stats, heatmap = bt.optimize(
        pb_buy=list(np.arange(0.1, 1.1, 0.1).round(1)),
        # pb_buy=list(np.arange(0.5, 1.1, 0.1).round(1)),++
        # mfi_pb_buy=list(np.arange(0.5, 1.1, 0.1).round(1)),
        mfi_pb_buy=list(np.arange(0.1, 1.1, 0.1).round(1)),
        maximize='Sharpe Ratio',
        return_heatmap=True
        # can also do a constraint, makes no sense for the upper bound to be less than lower bound
        # constraint=lambda param: param.upper_bound > param.lower_bound
    )
    print(stats)
    print('###################################')
    print(f"pb_buy {stats["_strategy"].pb_buy}")
    print(f"mfi_pb_buy {stats['_strategy'].mfi_pb_buy}")
    print('########################3333#######')
    print(heatmap)
    plot_heatmaps(heatmap, agg="mean")
    bt.plot(filename='DeMarkBBStrategy-optimized.html', open_browser=False)


def backtest_explore(bt):
    stats = bt.run()
    print(stats)
    ##### See what percent of data is covered in MFI bands
    s = stats._strategy
    df = pd.DataFrame({
        'mfi': s.mfi_panel[0],  # 2D indicator: row 0
        'mfi_bb_lower': s.mfi_panel[1],  # row 1
        'mfi_bb_upper': s.mfi_panel[2],  # row 2
        'percent_b': s.pb,
        'bb_squeeze': s.bb_squeeze,
        'bull_flip': s.bull_flip,
        'bb_lower': s.bb_lower_ind,
        'bb_higher': s.bb_higher_ind,
    }, index=stats['_equity_curve'].index)

    df_no_nan = df.dropna()
    mfi_in_bands = (df_no_nan['mfi'] > df_no_nan['mfi_bb_lower']) & (df_no_nan['mfi'] < df_no_nan['mfi_bb_upper'])
    print(f"MFI in bands: {mfi_in_bands.mean():.2%}")

    bt.plot(filename='DeMarkBBStrategy.html', open_browser=False)


def main():

    csv_path = Path("./trade/data/raw") / f"AAPL.csv"

    data = pd.read_csv(csv_path, index_col="Date", parse_dates=["Date"]).sort_index()
    data = data.dropna(subset=["Open", "High", "Low", "Close", "Volume"])


    bt = Backtest(data, DeMarkBBStrategy, cash=10_000, finalize_trades=True)
    backtest_explore(bt)
    # optim_explore(bt)


if __name__ == "__main__":
    main()
