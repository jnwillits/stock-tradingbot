from indicators import Indicator
import matplotlib.pyplot as plt


class MacdIndicator(Indicator):

    def plot(self, title):
        if 'MACD' not in self.data:
            self.calculate()

        columns = ['MACD', 'SIGNAL']
        self.data[columns].plot(figsize=(12.2, 4.5))
        plt.title(title)
        plt.xlabel('Date')
        plt.show()

    def calculate(
        self,
        shortterm_lookback_period=12, 
        longterm_lookback_period=26, 
        signal_lookback_period=9
    ):
        stlp_emas = self.data['Close'].ewm(span=shortterm_lookback_period, adjust=False).mean()
        ltlp_emas = self.data['Close'].ewm(span=longterm_lookback_period, adjust=False).mean()
        macds = stlp_emas - ltlp_emas
        signals = macds.ewm(span=signal_lookback_period, adjust=False).mean()

        self.data['MACD'] = macds
        self.data['SIGNAL'] = signals

        return macds, signals
