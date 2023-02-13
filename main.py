import os
import openai
import telebot
bot_token = os.environ['TOKEN']
openaiKey = os.environ['KEY']
openai.api_key = openaiKey
bot = telebot.TeleBot(bot_token, parse_mode=None)

def openia(mess):
    completion = openai.Completion.create(engine="text-davinci-003", 
                                          prompt=mess,
                                          max_tokens= 4000)
    return str(completion.choices[0].text)


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

"""@bot.message_handler(commands=['pdf'])
def send_pdf(message):
    cid=message.photo
    bot.send_chat_action(cid, 'typing')
    bot.reply_to(message, cid)

@bot.message_handler(commands=['photo'])
def photo(message):"""
    

bot.infinity_polling()
