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
                                          max_tokens= 3000)
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

bot.infinity_polling()
