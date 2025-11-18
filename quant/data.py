# quant/data.py
from dataclasses import dataclass
import yfinance as yf
import pandas as pd

@dataclass
class Bar:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class DataFeed:
    def iter_bars(self):
        """
        逐个产出 Bar:
        Bar(date, open, high, low, close, volume)
        """
        raise NotImplementedError
    
class YFinanceDataFeed(DataFeed):
    def __init__(self, symbol: str, start: str, end: str):
        self.symbol = symbol
        self.start = start
        self.end = end

    def iter_bars(self):
        try:
            df = yf.download(
                self.symbol,
                start=self.start,
                end=self.end,
                auto_adjust=True  # 用复权后的价格，避免分红拆股把曲线搞断
            )
            if df.empty:
                print(f"No data downloaded for {self.symbol} from {self.start} to {self.end}. Check symbol and date range.")
                return
        except Exception as e:
            print(f"Error downloading data for {self.symbol}: {e}")
            return

        # 确保按时间排序
        df = df.sort_index()

        # 只保留我们需要的列，并做简单前值填充
        df = df[["Open", "High", "Low", "Close", "Volume"]].ffill()

        for dt, row in df.iterrows():
            yield Bar(
                date=dt.strftime("%Y-%m-%d"),
                open=float(row["Open"].iloc[0]),
                high=float(row["High"].iloc[0]),
                low=float(row["Low"].iloc[0]),
                close=float(row["Close"].iloc[0]),
                volume=float(row["Volume"].iloc[0])
            )