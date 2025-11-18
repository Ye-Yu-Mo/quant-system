# quant/strategy/advanced.py

from collections import deque
import numpy as np
import pandas as pd
from typing import Optional

from ..data import Bar

# State object for the advanced strategy
class AdvancedStrategyState:
    def __init__(self, initial_position: float = 0.0):
        self.target_position = initial_position

# Layer 1: Feature
class Feature:
    def __init__(self):
        self.value = None

    def update(self, bar: Bar, history: pd.DataFrame):
        raise NotImplementedError

class MovingAverageFeature(Feature):
    def __init__(self, window: int):
        super().__init__()
        self.window = window

    def update(self, bar: Bar, history: pd.DataFrame):
        if len(history) >= self.window:
            self.value = history['close'].tail(self.window).mean()
        else:
            self.value = None

class VolatilityFeature(Feature):
    def __init__(self, window: int):
        super().__init__()
        self.window = window

    def update(self, bar: Bar, history: pd.DataFrame):
        if len(history) >= self.window:
            self.value = history['close'].tail(self.window).std()
        else:
            self.value = None

# Layer 2: Signal
class Signal:
    def __init__(self):
        self.value = None # The signal's output, e.g., a score or a boolean

    def update(self, bar: Bar, features: dict[str, Feature]):
        raise NotImplementedError

class MomentumSignal(Signal):
    def __init__(self, ma_feature_name: str):
        super().__init__()
        self.ma_feature_name = ma_feature_name

    def update(self, bar: Bar, features: dict[str, Feature]):
        ma = features[self.ma_feature_name].value
        if ma is not None:
            # Simple momentum: 1 if price is above MA, -1 if below
            if bar.close > ma:
                self.value = 1.0
            elif bar.close < ma:
                self.value = -1.0
            else:
                self.value = 0.0
        else:
            self.value = 0.0

class VolatilityFilter(Signal):
    def __init__(self, vol_feature_name: str, threshold: float):
        super().__init__()
        self.vol_feature_name = vol_feature_name
        self.threshold = threshold

    def update(self, bar: Bar, features: dict[str, Feature]):
        volatility = features[self.vol_feature_name].value
        if volatility is not None:
            # Signal is True (allow trading) if volatility is below threshold
            self.value = volatility < self.threshold
        else:
            self.value = False

# Layer 3: Position Sizer
class PositionSizer:
    def calculate_target_position(self, current_position: float, signals: dict[str, Signal]) -> float:
        raise NotImplementedError

class SimplePositionSizer(PositionSizer):
    def __init__(self, momentum_signal_name: str, vol_filter_name: Optional[str] = None, step: float = 0.1):
        super().__init__()
        self.momentum_signal_name = momentum_signal_name
        self.vol_filter_name = vol_filter_name
        self.step = step

    def calculate_target_position(self, current_position: float, signals: dict[str, Signal]) -> float:
        # Check volatility filter first, if provided
        if self.vol_filter_name:
            vol_filter_signal = signals.get(self.vol_filter_name)
            if vol_filter_signal and not vol_filter_signal.value:
                # If volatility is too high, do not change position
                return current_position

        momentum = signals[self.momentum_signal_name].value
        
        # Adjust position based on momentum signal
        if momentum > 0: # Price is above MA
            return min(1.0, current_position + self.step)
        elif momentum < 0: # Price is below MA
            return max(0.0, current_position - self.step)
        
        return current_position

# The main strategy class that combines everything
class AdvancedStrategy:
    def __init__(self, features: dict[str, Feature], signals: dict[str, Signal], position_sizer: PositionSizer):
        self.features = features
        self.signals = signals
        self.position_sizer = position_sizer
        self.history = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])

    def on_bar(self, bar: Bar, state: AdvancedStrategyState):
        # 1. Update history
        new_row = pd.DataFrame([bar.__dict__], index=[pd.to_datetime(bar.date)])
        if self.history.empty:
            self.history = new_row
        else:
            self.history = pd.concat([self.history, new_row])
        
        # 2. Update all features
        for feature in self.features.values():
            feature.update(bar, self.history)

        # 3. Update all signals
        for signal in self.signals.values():
            signal.update(bar, self.features)

        # 4. Calculate target position
        new_target_position = self.position_sizer.calculate_target_position(state.target_position, self.signals)
        state.target_position = new_target_position

        return new_target_position, state
