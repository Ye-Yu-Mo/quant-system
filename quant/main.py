import matplotlib.pyplot as plt

from .backtester import Backtester
from .data import YFinanceDataFeed
from .strategy.modular_strategy import (
    AdvancedStrategy,
    AdvancedStrategyState,
    MomentumSignal,
    MovingAverageFeature,
    SimplePositionSizer,
    VolatilityFeature,
    VolatilityFilter,
)

def main():
    """
    主函数，用于运行和对比两种策略配置。
    """
    # --- 1. 运行纯动量策略 ---
    print("--- 运行模块化策略: 仅动量 ---")
    feed_mom_only = YFinanceDataFeed(symbol="AAPL", start="2018-01-01", end="2024-01-01")
    bt_mom_only = Backtester(fee_rate=0.0005, slippage=0.0005)
    
    features_mom_only = {"ma50": MovingAverageFeature(window=50)}
    signals_mom_only = {"momentum": MomentumSignal(ma_feature_name="ma50")}
    sizer_mom_only = SimplePositionSizer(momentum_signal_name="momentum", step=0.05)
    
    strategy_mom_only = AdvancedStrategy(
        features=features_mom_only, 
        signals=signals_mom_only, 
        position_sizer=sizer_mom_only
    )
    initial_state_mom_only = AdvancedStrategyState(initial_position=0.0)
    
    equity_mom_only, _ = bt_mom_only.run(
        data_feed=feed_mom_only,
        strategy=strategy_mom_only,
        initial_state=initial_state_mom_only,
        initial_capital=100_000,
    )
    print(f"最终权益: {equity_mom_only['equity'].iloc[-1]:.2f}")

    # --- 2. 运行带波动率过滤的策略 ---
    print("\n--- 运行模块化策略: 动量 + 波动率过滤 ---")
    feed_with_vol = YFinanceDataFeed(symbol="AAPL", start="2018-01-01", end="2024-01-01")
    bt_with_vol = Backtester(fee_rate=0.0005, slippage=0.0005)

    features_with_vol = {
        "ma50": MovingAverageFeature(window=50),
        "vol20": VolatilityFeature(window=20),
    }
    signals_with_vol = {
        "momentum": MomentumSignal(ma_feature_name="ma50"),
        "vol_filter": VolatilityFilter(vol_feature_name="vol20", threshold=2.0),
    }
    sizer_with_vol = SimplePositionSizer(
        momentum_signal_name="momentum", 
        vol_filter_name="vol_filter",
        step=0.05
    )
    
    strategy_with_vol = AdvancedStrategy(
        features=features_with_vol, 
        signals=signals_with_vol, 
        position_sizer=sizer_with_vol
    )
    initial_state_with_vol = AdvancedStrategyState(initial_position=0.0)

    equity_with_vol, _ = bt_with_vol.run(
        data_feed=feed_with_vol,
        strategy=strategy_with_vol,
        initial_state=initial_state_with_vol,
        initial_capital=100_000,
    )
    print(f"最终权益: {equity_with_vol['equity'].iloc[-1]:.2f}")

    # --- 3. 在同一张图上绘制两条曲线 ---
    plt.figure(figsize=(12, 8))
    
    equity_mom_only['equity'].plot(label='Momentum Only', legend=True)
    equity_with_vol['equity'].plot(label='Momentum + Volatility Filter', legend=True)
    
    plt.title('Strategy Comparison on AAPL')
    plt.xlabel('Date')
    plt.ylabel('Equity')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()