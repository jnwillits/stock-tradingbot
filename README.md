
Jeff's TradeBot

Here is an awesome trade bot that sends trading signals to your email. The project started from a
version of TradeBot I forked from theryanle/stock-tradingbot on GitHub. It uses MACD and RSI
indicators to provide buy/sell/hold signals for trading of stocks.

My changes and enhancements include:

    1. Adding functionally to allow signals of multiple ticker symbols.
    2. Changing output from SMS messages via Twillo to emails.
    3. Providing an altered method of retrieving stock data.
    4. Adding a feaure to prevent output on a non-trading day.
    5. Added a log file for the output to facilitate back-testing of the signals.

I may add a graphic interface and allow multiple accounts so different stock ticker lists can be
stored in a database and relevant output can be sent to different emails. The intended usage of
this program is to execute a compiled version daily from a scheduler.

Jeff Willits  jnwillits.com



## Setup
1. Update the bot.py file with your email(s) and stock ticker symbols.
```
 tickers = ['ICE', 'CBSH', 'JNJ', 'SO', 'NVDA', 'ARKF']
 to_email = """ your_email_1@gmail.com;
                   your_email_2@gmail.com """ 
```
2. Compile the bot.py file into an executible file.
```
You can pip install PyInstaller and use the command:

pyinstaller bot.py --onefile

If you have problems with this, the easiest solution can be to find pyinstaller.exe on your drive
and place a copy in the same folder as the program files.

```
3. Use a scheduler, such as Microsoft Scheduler to run bot.ext daily.




## Requirements
+Python 3.7 and above



## Installation
Install the dependencies
```
pip install -r requirements.txt
```


## Usage
```
$ python bot.py
```
