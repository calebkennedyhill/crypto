import yfinance as yf
from pathlib import Path

def main():
    # the docker output path
    output_dir = Path("/app/raw")
    tickers = ['AAPL', 'MSFT', 'GOOG', "ETN", "BKNG", "QCOM", "PANW", "DHR", "BX", "LOW", "SYK", "SPGI", "CB", "INTU"]
    data = yf.download(tickers, start='2008-01-01', end='2020-01-01', multi_level_index=True)
    for ticker in data.columns.get_level_values('Ticker').unique():
        ticker_data = data.xs(ticker, axis='columns', level='Ticker')
        ticker_data.to_csv(output_dir/f"{ticker}.csv")


if __name__ == "__main__":
    main()
