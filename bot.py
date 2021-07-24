# !/usr/bin/env python
"""
Jeff's TradeBot
This started from a version of TradeBot forked from theryanle/stock-tradingbot on GitHub. It uses MACD and
RSI indicators to provide clear buy/sell/hold singles that may be useful for swing trading of stocks.

My changes include:
    1. Adding functionally to allow signals of multiple ticker symbols.
    2. Changing output from SMS messages via Twillo to emails.
    3. Altered method of retrieving stock data.
    4. Added feaure to prevent output on a non-trading day when the signal message does not change.

I plan to add a graphic interface and include a database for an output log to use for testing the stratgy.
Perhaps I will allow multiple accounts so different stock ticker lists can be stored in the database and 
relevant output can be sent to different emails. I may also restrict the program from sending emails after
non-trading days and add alerts when signals change. The intended usage of this program is to execute a 
compiled version daily from a scheduler.

Jeff Willits  jnwillits.com
"""

import win32com.client as win32
import json
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


def read_message_file():
    if os.path.isfile('last_message.json'):
        with open('last_message.json') as f_obj:
            return json.load(f_obj)
    

def write_message_file(total_message_pass):
    with open('last_message.json', 'w') as f_obj:
        json.dump(total_message_pass, f_obj)



if __name__ == '__main__':
   
    tickers = ['ICE', 'CBSH', 'JNJ', 'SO', 'NVDA', 'ARKF', 'SBNY', 'AMD', 'SQ', 'VMW']
    to_email = """ your_email_1@gmail.com;
                   your_email_2@@netscape.net """ 
   
    total_message = ''
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
        # Abort output if no change in message - nontrading day.
        if total_message == read_message_file():
            sys.exit()
        else:
            write_message_file(total_message)

    # mail
    outlook = win32.gencache.EnsureDispatch('Outlook.Application')
    new_mail = outlook.CreateItem(0)
    new_mail.Subject = f"Jeff's TradeBot Signals for {date.today():%m/%d/%y}"
    new_mail.Body = total_message
    new_mail.To = to_email
    new_mail.Send()
    sys.exit()
    
