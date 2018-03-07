
# CryptoWDBot
A telegram bot that periodically checks bitcoin price for fluctuations and sends an alert if it detects one.
# Installation
Either create a secret.py file containing `token='YOUR TOKEN'` or remove the `import secret` and replace `token=secret.token` with your token.
```
$ git clone https://github.com/HrBDev/CryptoWDBot.git
$ cd CryptoWDBot
$ python CryptoWatchdogBot.py
```
# Commands
watch :`/watch <Coin> <Seconds>` Example: `/watch ETC 7200`

help : shows description
