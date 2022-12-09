import os
from binance import Client
from telebot import TeleBot, types
from flask import Flask, request

TOKEN = os.environ.get('API_TOKEN', None)
APP_NAME = os.environ.get('APP_NAME', None)

bot = TeleBot(TOKEN)
server = Flask(__name__)
client = Client()

@bot.message_handler(commands=['start'], chat_types=['private'])
def startPrivate(msg : types.Message):
    bot.send_message(
        msg.chat.id,
        '<b>😄 Welcome To Our Bot Crypto Price EXP Bot All Data Is From https://binance.com\n\nUsage : /p btc</b>'.format(msg.from_user.first_name),
        parse_mode='html',
        reply_to_message_id=msg.id,
        disable_web_page_preview=True
    )

@bot.message_handler(func= lambda msg : msg.text.startswith('/p'))
def getPrice(msg):
    symbol = msg.text.split('/p ')
    if len(symbol) == 1:
        bot.send_message(msg.chat.id, '*Example : /p BTC*', parse_mode='markdown')
        return
    try:
        symbol_ = symbol[1].upper()
        result = client.get_ticker(symbol = f'{symbol_}USDT')
        current_price = result['lastPrice']
        price_change = result['priceChange']
        price_change_percentage = result['priceChangePercent']

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(text='🔁 Refresh', callback_data='refresh '+symbol_)
        )
        text_to_send = f'*💎 {symbol_} Price Today*\n\n➛ Price: *{str(current_price)}$*\n📉 Price Change: *{str(price_change)}$*\n🔴 Change Percent: *{str(price_change_percentage)}%*'

        bot.send_message(
            msg.chat.id,
            text_to_send,
            parse_mode='markdown',
            reply_markup=markup
        )
    except:
        bot.send_message(msg.chat.id, '*❌ This currency is not supported or either it is wrong!*', parse_mode='markdown')

@bot.callback_query_handler(func=lambda call : call.data.startswith('refresh'))
def callbackQueryHandler(call : types.CallbackQuery):
    symbol = call.data.split('refresh ')[1]

    result = client.get_ticker(symbol = f'{symbol}USDT')
    current_price = result['lastPrice']
    price_change = result['priceChange']
    price_change_percentage = result['priceChangePercent']

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text='🔁 Refresh', callback_data='refresh '+symbol)
    )
    text_to_send = f'*💎 {symbol} Price Today*\n\n➛ Price: *{str(current_price)}$*\n📉 Price Change: *{str(price_change)}$*\n🔴 Change Percent: *{str(price_change_percentage)}%*'


    bot.edit_message_text(
        chat_id=call.message.chat.id,
        text= text_to_send,
        message_id=call.message.id,
        reply_markup=markup,
        parse_mode='markdown'
    )

bot.infinity_polling()
