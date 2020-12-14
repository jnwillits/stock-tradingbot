import numpy as np
import pandas as pd
import logging
from datetime import datetime
import pandas_datareader as pdr
from enums.signal import Signal
from twilio.rest import Client
from dateutil.relativedelta import relativedelta
from config.credentials import (
    twilio_number, twilio_account_sid, twilio_auth_token
)
from indicators import MacdIndicator, RsiIndicator
from strategies import Strategy, MacdRsiStrategy


logger = logging.getLogger('TradeBot')


class TradeBot:

    def __init__(self):
        self._strategy = None
        self._source = 'yahoo'

    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, value: Strategy):
        self._strategy = value

    def get_stock_data(self, ticker: str, start: str, end: str):
        try:
            data = pdr.DataReader(
                ticker.upper(), data_source=self._source,
                start=start, end=end
            )
        except Exception as error:
            logger.error(f'Fail to fetch {ticker} data from source!', error)
            return None
        else:
            return data

    def get_trade_signal(self):
        try:
            signal = self.strategy.execute()
        except Exception as error:
            logger.error(f'Fail to get trade signal using {self.strategy.name}!', error)
            signal = None
        finally:
            return signal


if __name__ == '__main__':
    
    ticker = 'UBER'
    phone_number = 'PHONE_NUMBER_GOES_HERE'
    bot = TradeBot()
    today = datetime.today()
    six_months_ago = today + relativedelta(months=-6)

    # query stock data
    data = bot.get_stock_data(ticker, str(six_months_ago), str(today))
    print(data)

    # indicators
    macd = MacdIndicator(data)
    rsi = RsiIndicator(data)

    # set strategy
    bot.strategy = MacdRsiStrategy(macd, rsi)
    signal = bot.get_trade_signal()
    
    result = {
        'Time': today.strftime('%m/%d/%Y at %H:%M:%S'),
        'Stock': ticker,
        'Signal': signal.name,
        'Price': round(data['Close'][-1], 3)
    }
    
    message = ""
    for k, v in result.items():
        message += f'{k}: {v} \n'

    print(message)

    # Send signal messages via SMS
    client = Client(twilio_account_sid, twilio_auth_token)
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=phone_number
    )

    print('message sent!')


