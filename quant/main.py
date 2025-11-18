from .data import YFinanceDataFeed
from .strategy import SimpleDCAStrategy
from .backtester import Backtester

import matplotlib.pyplot as plt


def main():
    feed = YFinanceDataFeed(
        symbol="AAPL",
        start="2015-01-01",
        end="2022-01-01",
    )

    strategy = SimpleDCAStrategy(window=20, step=0.04)
    bt = Backtester(fee_rate=0.0005, slippage=0.0005)

    equity, trades = bt.run(feed, strategy, initial_capital=100_000)

    print("起始资金：", 100_000)
    print("结束资金：", round(equity["equity"].iloc[-1], 2))
    print("整体收益率：", round(equity["equity"].iloc[-1] / 100_000 - 1, 4))

    equity["equity"].plot(figsize=(12, 6))
    plt.title("Simple DCA Strategy on AAPL")
    plt.ylabel("Equity")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()