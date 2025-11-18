# quant/strategy/base.py

from ..data import Bar

class Strategy:
    """
    所有策略的基类，定义了策略必须实现的接口。
    """
    def on_bar(self, bar: Bar, state):
        """
        每个 bar 调用一次的核心方法。

        Args:
            bar (Bar): 当前的市场数据。
            state: 策略的内部状态对象，用于在 bar 之间传递信息。

        Returns:
            tuple: (目标仓位比例, 更新后的状态对象)
                   目标仓位比例是一个在 0.0 到 1.0 之间的浮点数。
        """
        raise NotImplementedError
