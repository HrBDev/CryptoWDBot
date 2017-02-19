import logging
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler, Job, Updater


def description(bot, update):
    '''Displays bot's description.'''
    txt = 'A telegram bot that periodically checks bitcoin price for fluctuations and sends an alert if it detecs one.'
    bot.sendMessage(chat_id=update.message.chat_id, text=txt)


def btcp(bot, job):
    '''Checks bitcoin price and stores it in a list.'''
    # Downloads the page
    page = requests.get('https://coinmarketcap.com/')
    date = datetime.now(timezone.utc).strftime("%Y %m %d %H:%M:%S UTC")
    # soup object
    soup = BeautifulSoup(page.content, 'html5lib')
    # finds btc price from soup object
    btc = soup.find('a', {'href': '/currencies/bitcoin/#markets'})
    # converting string to int after removing $ and . from it
    price = int(btc.string.replace('$', '').replace('.', '')) / 100
    pricelist.append(price)
    alert = 'BTC price fluctuation detected.\nPrice 30 minutes ago: ${}\nPrice now: ${}\nLast updated: {}'.format(
        pricelist[-2], pricelist[-1], date)
    if pricelist[-2] - pricelist[-1] >= 2:
        bot.sendMessage(job.context, text=alert)
    elif pricelist[-1] - pricelist[-2] > 2:
        bot.sendMessage(job.context, text=alert)


def watchbtc(bot, update, args, job_queue, chat_data):
    '''Adds btcp to the queue.'''
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            bot.sendMessage(
                chat_id=chat_id, text='Sorry we can not go back to future!')
            return

        # Add job to queue
        job = Job(btcp, due, repeat=True, context=chat_id)
        chat_data['job'] = job
        job_queue.put(job)

        bot.sendMessage(chat_id, 'Timer successfully set!')

    except (IndexError, ValueError):
        bot.sendMessage(chat_id, 'Usage: /watchbtc <seconds>')


def main():
    '''Main funtion.'''

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    token = 'TOKEN'
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('help', description))
    updater.dispatcher.add_handler(
        CommandHandler(
            'watchbtc',
            watchbtc,
            pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True))

    global pricelist
    # 0s are dummy values
    pricelist = [0, 0]

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
