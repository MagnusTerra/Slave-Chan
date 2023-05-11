import os
import openai
import telebot
from telebot import types
from contantes import *
bot_token = os.environ['TOKEN']
openaiKey = os.environ['KEY']
openai.api_key = openaiKey
bot = telebot.TeleBot(bot_token, parse_mode=None)

def openia(mess):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": {mess}}])
    return str(completion.choices[0].text)


def openimage(mess):
    image_resp = openai.Image.create(prompt=mess, n=2, size="1024x1024")
    image_url = image_resp['data'][0]['url']
    return str(image_url)

@bot.message_handler(commands=['q'])
def send_welcome(message):
    cid=message.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.reply_to(message, openia(message.text))


@bot.message_handler(commands=['start'])
def send_start(message):
    cid=message.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.reply_to(message, "Hola")

@bot.message_handler(commands=['i'])
def send_Image(message):
    cid=message.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.reply_to(message, openimage(message.text)) 

@bot.message_handler(commands = ['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Dame un Cafe', url='https://ko-fi.com/moviesall')
    markup.add(btn_my_site)
    bot.send_photo(-1001624656642, 'https://t.me/WallpaersChidos/212')
    bot.send_message(-1001624656642, donaciones, reply_markup = markup)   

@bot.message_handler(commands=['getid'])
def getid(message):
    cid= message.channel.id
    bot.send_message(cid, str(cid))
bot.infinity_polling()

