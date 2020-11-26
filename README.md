
An awesome trade bot that sends trading signals to your phone.

## Setup
1. Signup for Twilio account at https://www.twilio.com/
2. Get an Account SID and Token, insert into config/credentials.py
```
twilio_number = 'TWILIO_PHONE_NUMBER'
twilio_account_sid = 'TWILIO_ACCOUNT_SID'
twilio_auth_token = 'TWILIO_AUTH_TOKEN'
```
3. Update the bot.py file with your phone number and the stock ticker symbol
```
ticker = 'STOCK_TICKER_SYMBOL'
phone_number = 'A_PHONE_NUMBER'
```

## Requirements
+Python 3.7 and above
+Twilio account

## Installation
Install the dependencies
```
pip install -r requirements.txt
```

## Usage
```
$ python bot.py
```
