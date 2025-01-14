
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
this program is to execute a compiled version daily from a scheduler such as Windows Task
Scheduler.

Jeff Willits  jnwillits.com



## Setup

1. Update the bot.py file with your email(s) and stock ticker symbols.
```
   tickers = ['ICE', 'CBSH', 'JNJ', 'SO', 'NVDA', 'ARKF']
   to_email = """ your_email_1@gmail.com;
                  your_email_2@gmail.com """ 
```

2. Compile the bot.py file into an executible file. You can pip install PyInstaller and use the
   command:

```
   pyinstaller bot.py --onefile
```

    If you have problems with this, the easiest solution can be to find pyinstaller.exe on your drive
    and place a copy in the same folder as the program files. Otherwise, it is not essential to run 
    this from a compiled file. You can run the script from python as:

    
```
   python bot.py
```


3. Use a scheduler, such as Windows Task Scheduler to run bot.ext daily. There can be issues 
   with file paths when using the scheduler. I solved this by running botbatch.bat instead of
   bot.exe from the scheduler. Before running the executable, the working directory is
   changed to the folder where the program data files reside. My file "botbatch.bat" is 
   included with the files, but you will need to revise the path command. If you leave your
   computer in sleep mode, be sure to set the scheduler to wake the computer to run the task.


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


## Having trouble with the email not generating? From PowerShell:
```
Remove-Item -path $env:LOCALAPPDATA\Temp\gen_py -recurse
```

I run this from a batch file and added this command to botbatch.bat. When running this 
command in a batch file from the Windows Task Scheduler, be sure to configure the
Scheduler for Windows 10, instead of an earlier version and have Powershell as the
default command prompt.
