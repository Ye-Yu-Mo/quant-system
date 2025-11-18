# quant/backtester.py

import numpy as np
import pandas as pd

from .data import DataFeed, Bar
from .strategy import Strategy, SimpleDCAState

class Backtester:
    def __init__(self, fee_rate: float = 0.0005, slippage: float = 0.0005):
        # 手续费 + 滑点，先用一个偏乐观但不离谱的数
        self.fee_rate = fee_rate
        self.slippage = slippage

    def run(self, data_feed: DataFeed, strategy: Strategy, initial_capital: float = 100_000):
        cash = initial_capital
        position_shares = 0.0
        equity_curve = []
        dates = []
        trades = []

        state = SimpleDCAState()
        last_price = None

        for bar in data_feed.iter_bars():
            price = bar.close

            if last_price is None:
                last_price = price

            # 账户当前总价值（用上一根价格估）
            current_equity = cash + position_shares * last_price

            # 让策略决定目标仓位比例
            target_weight, state = strategy.on_bar(bar, state)

            # 目标持仓金额 & 股数
            target_position_value = current_equity * target_weight
            target_shares = target_position_value / price if price > 0 else 0.0

            # 需要调整的股数
            delta_shares = target_shares - position_shares

            # 粗糙的滑点模型：买入抬价，卖出压价
            if abs(delta_shares) > 1e-8:
                trade_price = price * (1 + self.slippage * np.sign(delta_shares))
                trade_value = delta_shares * trade_price
                fee = abs(trade_value) * self.fee_rate
            else:
                trade_price = price
                trade_value = 0.0
                fee = 0.0

            # 更新现金和持仓
            cash -= trade_value + fee
            position_shares = target_shares
            last_price = price

            # 当前权益 = 现金 + 持仓市值
            total_equity = cash + position_shares * price
            dates.append(bar.date)
            equity_curve.append(total_equity)

            if abs(delta_shares) > 1e-6:
                trades.append({
                    "date": bar.date,
                    "price": trade_price,
                    "shares": delta_shares,
                    "fee": fee,
                    "equity": total_equity
                })

        equity_df = pd.DataFrame({"date": dates, "equity": equity_curve}).set_index("date")
        trades_df = pd.DataFrame(trades)

        return equity_df, trades_df
