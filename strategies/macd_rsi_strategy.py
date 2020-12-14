from enums.signal import Signal
from indicators import MacdIndicator, RsiIndicator
from strategies import Strategy
from common.exceptions import StrategyException


class MacdRsiStrategy(Strategy):

    def __init__(self, macd: MacdIndicator, rsi: RsiIndicator):
        self._macd = macd
        self._rsi = rsi
    
    @property
    def name(self):
        return self.__class__.__name__

    def execute(self) -> Signal:
        macds, signals = self._macd.calculate()
        rsis = self._rsi.calculate()
        
        last_macd, last_signal = macds[-1], signals[-1]
        last_rsi = rsis[-1]
        
        if last_macd > last_signal and last_rsi < self._rsi.overbought:
            signal = Signal.BUY
        elif last_macd < last_signal and last_rsi > self._rsi.oversold:
            signal = Signal.SELL
        else:
            signal = Signal.HOLD

        return signal



