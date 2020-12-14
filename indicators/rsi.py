from pandas import DataFrame
from indicators import Indicator
import matplotlib.pyplot as plt


class RsiIndicator(Indicator):

    def __init__(self, data: DataFrame, overbought: int = 70, oversold: int = 30):
        super().__init__(data)
        self.overbought = overbought
        self.oversold = oversold

    def plot(self, title):
        if 'RSI' not in self.data:
            self.calculate()

        self.data['RSI'].plot(figsize=(12.2, 4.5))
        plt.title(title)
        plt.xlabel('Date')
        plt.axhline(y=self.overbought, color='r', linestyle='-')
        plt.axhline(y=self.oversold, color='g', linestyle='-')
        plt.show()

    def calculate(self, period=14):
        delta = self.data['Close'].diff(1)
        delta = delta[1:]
        up = delta.copy()
        down = delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        avg_gain = up.ewm(span=period, adjust=False).mean()
        avg_loss = abs(down.ewm(span=period, adjust=False).mean())
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0/(1.0+rs))

        self.data['RSI'] = rsi

        return rsi
