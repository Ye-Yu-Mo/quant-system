from .data import YFinanceDataFeed
from .strategy.dca_strategy import SimpleDCAStrategy
from .strategy.modular_strategy import (
    MovingAverageFeature,
    VolatilityFeature,
    MomentumSignal,
    VolatilityFilter,
    SimplePositionSizer,
    AdvancedStrategy,
    AdvancedStrategyState,
)
from .backtester import Backtester

import matplotlib.pyplot as plt


def main():
    feed = YFinanceDataFeed(
        symbol="AAPL",
        start="2015-01-01",
        end="2025-01-01",
    )

    # --- Simple Strategy (commented out) ---
    # from .strategy.simple import SimpleDCAState
    # strategy = SimpleDCAStrategy(window=20, step=0.04)
    # initial_state = SimpleDCAState(window=20)
    # title = "Simple DCA Strategy on AAPL"

    # --- Advanced Modular Strategy ---
    features = {
        "ma50": MovingAverageFeature(window=50),
        "vol20": VolatilityFeature(window=20),
    }
    
    signals = {
        "momentum": MomentumSignal(ma_feature_name="ma50"),
        "vol_filter": VolatilityFilter(vol_feature_name="vol20", threshold=2.0) # Example of adding a filter
    }

    position_sizer = SimplePositionSizer(
        momentum_signal_name="momentum",
        vol_filter_name="vol_filter",
        step=0.05
    )

    strategy = AdvancedStrategy(
        features=features,
        signals=signals,
        position_sizer=position_sizer,
    )
    initial_state = AdvancedStrategyState(initial_position=0.0)
    title = "Advanced Modular Strategy on AAPL (with Volatility Filter)"


    bt = Backtester(fee_rate=0.0005, slippage=0.0005)

    equity, trades = bt.run(
        data_feed=feed,
        strategy=strategy,
        initial_state=initial_state,
        initial_capital=100_000
    )

    if equity.empty:
        print("回测结束，但没有生成权益曲线。可能原因：数据下载失败或策略未产生任何交易。")
        return

    print("起始资金：", 100_000)
    print("结束资金：", round(equity["equity"].iloc[-1], 2))
    print("整体收益率：", round(equity["equity"].iloc[-1] / 100_000 - 1, 4))

    equity["equity"].plot(figsize=(12, 6))
    plt.title(title)
    plt.ylabel("Equity")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()