import numpy as np
import pandas as pd
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from enums.signal import Signal
from twilio.rest import Client
from indicators import Indicator, MacdIndicator
from dateutil.relativedelta import relativedelta
from common.exceptions import IndicatorException
from config.credentials import (
    twilio_number, twilio_account_sid, twilio_auth_token
)

logger = logging.getLogger('TradeBot')


class TradeBot:
    def __init__(self, indicator: Indicator):
        self._indicator = indicator
        self._source = 'yahoo'

    @property
    def indicator(self):
        return self._indicator
    
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

    def get_trade_signal(self, ticker: str):
        today = datetime.today()
        six_months_ago = today + relativedelta(months=-6)
        data = self.get_stock_data(ticker, str(six_months_ago), str(today))
        if data is None:
            logger.error(f'No data found for {ticker}')
            return data

        last_trade = data.to_dict('records')[-1]
        try:
            if self.indicator.execute(data):
                last_buy_signal = self.indicator.get_buy_signals(last_result=True)
                last_sell_signal = self.indicator.get_sell_signals(last_result=True)
            else:
                raise RuntimeError(f'Fail to analyze {ticker} data')
        except IndicatorException as error:
            logger.error(f'Fail to get trade signal for ticker symbol: {ticker}!', error)
            return None
        else:
            if last_buy_signal:
                signal = Signal.BUY
            elif last_sell_signal:
                signal = Signal.SELL
            else:
                signal = Signal.UNKNOWN

        timestamp = today.strftime('%m/%d/%Y at %H:%M:%S')
        result = {'Time': timestamp, 'Stock': ticker, 'Signal': signal.name}
        result.update(last_trade)

        return result


if __name__ == '__main__':
    # Client code 
    ticker = 'STOCK_TICKER_SYMBOL'
    phone_number = 'A_PHONE_NUMBER'
    # Initialize with MACD indicator
    bot = TradeBot(indicator=MacdIndicator())
    signal = bot.get_trade_signal(ticker)

    message = ""
    for k, v in signal.items():
        message += f'{k}: {v} \n'

    # Send signal messages via SMS
    try:
        client = Client(twilio_account_sid, twilio_auth_token)
        client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )
    except Exception as error:
        print(f'Fail to send text message to {phone_number}!', error)
    else:
        print(message)
        print('message sent!')
