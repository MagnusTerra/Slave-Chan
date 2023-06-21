import os
import openai
import telebot
from telebot import types
from contantes import *
from ocrtest import *

# Establecer las variables del sistema
bot_token = os.environ['TOKEN']
openaiKey = os.environ['KEY']
openai.api_key = openaiKey
bot = telebot.TeleBot(bot_token, parse_mode=None)

# Esta funcion nos permite usar la API de OpenAI para usar ChatGPT
def openia(mess):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": mess}])
    return str(completion.choices[0].message.content)


def openimage(mess):
    image_resp = openai.Image.create(prompt=mess, n=2, size="1024x1024")
    image_url = image_resp['data'][0]['url']
    return str(image_url)

@bot.message_handler(commands=['q'])
def send_welcome(message):
    try:
        cid=message.chat.id
        bot.send_chat_action(cid, 'typing')
        bot.reply_to(message, openia(message.text))
    except Exception as e:
        bot.send_message(1144864634, e)


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

# Esta funcion manda el ChatID del chat 
@bot.message_handler(commands=['thischatid'])
def getid(message):
    cid = message.chat.id
    bot.send_message(cid, f'Este es el el ID de este Chat {cid}')

# Este evento se ejecutara cuando registre una imagen con un caption de ocr
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    cid = message.chat.id
    cid2 = message.message_thread_id

    if str(message.caption) == 'ocr':
        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        file_path = photo_info.file_path
        file = bot.download_file(file_path)
        file_name = f'{cid}.jpg'

        with open(file_name, 'wb') as photo:
            photo.write(file)
            
        text = ocr_horizontal(str(file_name))
        bot.send_chat_action(cid, 'typing')
        transl = openia(str(f'Traduce este texto al español y haz que tenga sentido: {text}'))
        if bot.send_message(cid, transl, cid2):
            os.remove(file_name)
    
    else:
        pass


#Esta funcion manda un txt con la informacion completa del mensaje 
@bot.message_handler(commands=['infomess'])
def inf_mess(message):
    chat_id = message.chat.id
    file_name = f'{chat_id}.txt'
    message_content = str(message)

    with open(file_name, 'w') as file:
        file.write(message_content)

    with open(file_name, 'rb') as document:
        bot.send_document(chat_id, document)

    os.remove(file_name)


# Esto mantiene el bot ejecutandoce 
bot.infinity_polling()

