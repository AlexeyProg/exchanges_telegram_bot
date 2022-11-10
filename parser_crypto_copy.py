
import requests
import telebot
from bs4 import BeautifulSoup
from pybit import inverse_perpetual
import pybit
from config_keys_crypto import *
from telebot import types
from binance.client import Client


info_banner = 'По всем вопросам и предложениям обращаться - @keeper_of_the_farm 🫡'


def scrap_site(url,coin_class):
    request = requests.get(url)
    soup = BeautifulSoup(request.text,'html.parser')
    coin_info = soup.find('div', class_=coin_class).text
    return coin_info


def bybit_api():
    key = api_key_bybit #your bybit api key
    secret = api_secret_bybit #your api secret bybit
    session = inverse_perpetual.HTTP(endpoint='https://api.bybit.com',api_key=key,
                                api_secret=secret)  
    ws = inverse_perpetual.WebSocket(test=False,api_key=key,api_secret=secret)
    info_coin = session.latest_information_for_symbol(symbol='BTCUSD')
    result_str = info_coin['result']
    str = result_str[0]
    ask_price = str['ask_price']
    return ask_price


#many functions for yobit  3 pieces  ******************************
def yobit_api():
    key = api_key_yobit #your key yobit
    secret = api_secret_yobit #your api secret yobit


def get_info():
    response = requests.get(url='https://yobit.net/api/3/info')
    with open('/Users/sokol/Desktop/python_proj/url.html','w') as f:
        f.write(response.text)
    return response.text


def get_ticket(pair):
    response = requests.get(url=f'https://yobit.net/api/3/ticker/{pair}')
    bid = response.json()

    price = bid[pair]['sell']
    final_price = int(price)
    return final_price
#yobit functions ended here **************************************



url_binance = 'https://www.binance.com/en/markets'
#bybit - api , yobit - api


bot = telebot.TeleBot(bot_key) #bot key - telegram bot api key

@bot.message_handler(commands=["start"])
def test_a(message):
    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('💵btc-usdt💵')
    item_info = types.KeyboardButton('ℹ️Информацияℹ️')

    markup.add(item1,item_info)

    #message_sender
    bot.send_message(message.chat.id,"Ready",reply_markup=markup, parse_mode='html')
    


@bot.message_handler(content_types=['text'])
def send_btc(message):
    if (message.text == '💵btc-usdt💵'):
        client = Client(api_key_binance1,api_secret_binance1) #your api key and secret binance
        coin_name = "BTCUSDT"
        binance_price = client.get_symbol_ticker(symbol=coin_name)
        binance_result = binance_price["price"]
        new_str_binance = binance_result[:-6]   # отрезаем лишние нули с конца, если что это строка! с цифрами


        #bybit
        bybit_info = bybit_api()

        #yobit
        yobit_price = get_ticket('btc_usdt')

        #message_sender
        bot.send_message(message.chat.id,f'Binance - {new_str_binance}$\nBybit - {bybit_info}$\nYobit - {yobit_price}$',
        parse_mode='html')

    elif (message.text == 'ℹ️Информацияℹ️'):
        bot.send_message(message.chat.id,info_banner)

    else:
        bot.send_message(message.chat.id,"Error! Unknown command!", parse_mode='html')
    

bot.polling()
