# quant/strategy.py

from .data import Bar
from collections import deque
import numpy as np
from .data import Bar

class Strategy:
    def on_bar(self, bar: Bar, state):
        """
        根据当前 bar + 内部状态
        返回 (目标仓位比例, 新状态)
        目标仓位比例通常在 0.0 ~ 1.0 之间
        """
        raise NotImplementedError
    
class SimpleDCAState:
    def __init__(self, window: int = 20):
        self.window = window
        self.prices = deque(maxlen=window)
        self.position = 0.0  # 目标仓位比例：0.0 ~ 1.0


class SimpleDCAStrategy(Strategy):
    def __init__(self, window: int = 20, step: float = 0.04):
        self.window = window
        self.step = step

    def on_bar(self, bar: Bar, state: SimpleDCAState):
        # 更新历史价格
        state.prices.append(bar.close)

        # 数据不足，不开仓
        if len(state.prices) < self.window:
            return state.position, state

        ma = float(np.mean(state.prices))

        # 简单规则：
        # 当前价比 MA 低 2% 以上 → 加一档仓位
        # 当前价比 MA 高 2% 以上 → 减一档仓位
        if bar.close < ma * 0.98:
            state.position = min(1.0, state.position + self.step)
        elif bar.close > ma * 1.02:
            state.position = max(0.0, state.position - self.step)

        return state.position, state