from .base import Indicator
from common.exceptions import IndicatorException
from enums.signal import Signal


class MacdIndicator(Indicator):
    def __init__(self):
        self._buys = []
        self._sells = []
    
    def _get_ema(self, data, period):
        return data.ewm(span=period, adjust=False).mean()

    def get_buy_signals(self, last_result=False):
        if not self._buys:
            raise IndicatorException('No buy signal found!')

        if last_result:
            return self._buys[-1] 
        else:
            return self._buys

    def get_sell_signals(self, last_result=False):
        if not self._sells:
            raise IndicatorException('No sell signal found!')

        if last_result:
            return self._sells[-1] 
        else:
            return self._sells

    def execute(self, data, shortterm_lookback_period=12, longterm_lookback_period=26):
        try:
            crossed = True
            stlp_emas = self._get_ema(data['Close'], shortterm_lookback_period)
            ltlp_emas = self._get_ema(data['Close'], longterm_lookback_period)
            macds = stlp_emas - ltlp_emas                # macds
            semas = self._get_ema(macds, period=9)       # 9-day signal moving average
            
            for macd, sema in zip(macds, semas):
                if macd > sema and crossed is False:
                    self._buys.append(True)
                    self._sells.append(False)
                    crossed = True
                elif macd < sema and crossed is True:
                    self._buys.append(False)
                    self._sells.append(True)
                    crossed = False
                else:
                    self._buys.append(False)
                    self._sells.append(False)
        except Exception as error:
            raise IndicatorException('Could not get macd signal!') from error
        else:
            return True

