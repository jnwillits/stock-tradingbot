# !/usr/bin/env python
"""
Jeff's TradeBot
This started from a version of TradeBot forked from theryanle/stock-tradingbot on GitHub. It uses MACD and
RSI indicators to provide clear buy/sell/hold singles that may be useful for swing trading of stocks.
My changes include:
    1. Adding functionally to allow signals of multiple ticker symbols.
    2. Changing output from SMS messages via Twillo to emails.
    3. Method in retrieving stock data.
    4. Adding timing to provide daily output via email.
I plan to add a graphic interface and include a database for an output log to use for testing the stratgy.
Perhaps I will allow multiple accounts so different stock ticker lists can be stored in the database and 
relevant output can be sent to different emails. I may also restrict the program from sending emails after
non-trading days and add alerts when signals change.

Jeff Willits  jnwillits.com
"""

import time
import win32com.client as win32
import sys
import os
from pathlib import Path
from datetime import date
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from enums.signal import Signal
from dateutil.relativedelta import relativedelta
from indicators import MacdIndicator, RsiIndicator
from strategies import Strategy, MacdRsiStrategy
from pandas_datareader import data as web


logger = logging.getLogger('TradeBot')

class TradeBot:

    def __init__(self):
        self._strategy = None

    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, value: Strategy):
        self._strategy = value

    def get_stock_data(self, ticker: str, start: str, end: str):
        try:
            data = web.get_data_yahoo(ticker.upper(), start=start, end=end)
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
    tickers = ['ICE', 'CBSH', 'JNJ', 'SO', 'NVDA', 'ARKF', 'SBNY', 'AMD', 'SQ', 'VMW']
    total_message = ''
    to_email = """ jeff.willits@live.com;
                   jeffrey0056@netscape.net """ 
    starttime=time.time()
    interval=86400 # 24 hour interval
    while True:
        for i in range (0, len(tickers)):
            ticker = tickers[i]
            bot = TradeBot()
            today = datetime.today()
            six_months_ago = today + relativedelta(months=-6)
            data = bot.get_stock_data(ticker, str(six_months_ago), str(today))
            # indicators
            macd = MacdIndicator(data)
            rsi = RsiIndicator(data)
            # strategy
            bot.strategy = MacdRsiStrategy(macd, rsi)
            signal = bot.get_trade_signal()
            # output
            message = ''
            message = f"{signal.name}  {ticker}  @  {round(data['Close'][-1], 3)}"
            total_message = total_message + '\n' + message    
        # mail
        outlook = win32.gencache.EnsureDispatch('Outlook.Application')
        new_mail = outlook.CreateItem(0)
        new_mail.Subject = f"Jeff's TradeBot Signals for {date.today():%m/%d/%y}"
        new_mail.Body = total_message
        new_mail.To = to_email
        new_mail.Send()

        time.sleep(interval - ((time.time() - starttime) % interval))
    sys.exit()
    
