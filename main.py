import os
import openai
import telebot
from telebot import types
from contantes import *
from ocrtest import *
from imgs import *
from get import *
from download import *
from img_pdf import *
from funcs import *
import shutil
from downloader import *
from buttons import *
import time
# Establecer las variables del sistema
bot_token = os.environ['TOKEN']
openaiKey = os.environ['KEY']
openai.api_key = openaiKey
bot = telebot.TeleBot(bot_token, parse_mode=None)

temp_dir = 'temp_images'
image_counters = {}
bot.set_my_commands(commands = [
    telebot.types.BotCommand('start', 'Comando de inicio del Bot'),
    telebot.types.BotCommand('pdf', 'Convertir imgs a PDF')
])
os.makedirs(temp_dir, exist_ok=True)

user_actions = {}
image_counters = {}


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

# Definición de función que maneja el comando '/thischatid'
@bot.message_handler(commands=['thischatid'])
def getid(message):
    cid = message.chat.id # Almacenar el ID del chat en la variable cid
    bot.send_message(cid, f'Este es el el ID de este Chat {cid}') # Responder al mensaje con el ID del chat usando la variable cid

# Este evento se ejecutara cuando registre una imagen con un caption de ocr
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    user_id = message.chat.id
    cid = message.chat.id   # Obtenemos el ID del chat donde se recibió el mensaje
    cid2 = message.message_thread_id   # Obtenemos el ID del hilo de mensajes donde se recibió el mensaje
    caption = str(message.caption)   # Convertimos la leyenda en una cadena de texto (si existe)

    # Verifica si el caption es "ocr"
    if caption == "ocr":
        # Obtener la información de la foto
        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        file_path = photo_info.file_path
        # Nombre del archivo y descarga del archivo a local
        file_name = f"{cid}.jpg"
        file = bot.download_file(file_path)
        
        with open(file_name, "wb") as photo:
            photo.write(file)
        
        text = ocr_horizontal(file_name) # Aplicar la función OCR para reconocimiento de texto en la foto
        
        bot.send_chat_action(cid, "typing") # Envía un mensaje de "escribir" para dar la impresión de que el bot está escribiendo
        transl = openia(f"Traduce este texto al español y haz que tenga sentido: {text}") # Aplica la función openia para traducir el texto en la foto a español

        bot.send_message(cid, transl, cid2)# Envía el texto traducido al usuario
        os.remove(file_name) # Elimina el archivo descargado
   
    # Verifica si el caption es "st"
    elif caption == "st":
        # Obtener la información de la foto
        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        file_path = photo_info.file_path
        # Nombre del archivo y descarga del archivo a local
        file_name = f"{cid}img.jpg"
        file = bot.download_file(file_path)

        with open(file_name, "wb") as photo:
            photo.write(file)

        # Redimensiona la foto y la guarda en formato PNG
        resize_img(file_name, f"{cid}")
        # Abre el archivo con formato PNG y lo envía al usuario
        with open(f"{cid}.png", "rb") as img:
            bot.send_document(cid, img, cid2)

        # Elimina los archivos descargados
        os.remove(file_name)
        os.remove(f"{cid}.png")

    try:
        if user_actions[user_id] == 'pdf':
            chat_dir = os.path.join(temp_dir, str(user_id))
            os.makedirs(chat_dir, exist_ok=True)
            # Download the photo
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            #time.sleep(0.20)   
            file_path = os.path.join(chat_dir, f"{image_counters[user_id]}.png")
            image_counters[user_id] += 1
            with open(file_path, 'wb') as file:
                file.write(downloaded_file)
            bot.reply_to(message, 'Imagen descargada')
            time.sleep(0.25) 
    except:
        pass

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

@bot.message_handler(commands=['nh'])
def nhentai(message):
    cid = message.chat.id
    cid2 = message.message_thread_id
    text = message.text.split(' ')
    try:
        path = f'bz/{cid}/{text[1]}'
        process_count = 30
        mess0 = bot.send_message(cid, 'Descargando Dōjinshi', message_thread_id = cid2)
        NhentaiDownloader(int(text[1]), process_count, path)
        bot.delete_message(cid, mess0.message_id, cid2)
        mess2 = bot.send_message(cid, 'Dōjinshi descargado Convirtiendo a pdf', message_thread_id = cid2)
    except:
        bot.delete_message(cid, mess0.message_id, cid2)
        bot.send_message(cid, 'No se encontro Dōjinshi')
    try:
        imgs_to_pdf(f'bz/{cid}/{text[1]}',str(cid))
        reduce_pdf_size(f'{cid}.pdf')
        with open(f"{cid}.pdf_decude.pdf", 'rb') as document:
            bot.send_document(cid, document, cid2)
        bot.delete_message(cid,mess2.message_id, cid2)
        os.remove(f'{cid}.pdf')
        os.remove(f'{cid}.pdf_decude.pdf')
        
        shutil.rmtree(f'bz/{str(cid)}')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['pdf'])
def handle_pdf(message):
    user_id = message.chat.id
    user_actions[user_id] = 'pdf'
    image_counters[user_id] = 1
    markup = pdf_buttons()
    bot.send_message(chat_id=user_id, text="Envia las Fotos para hacelas PDF", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_all_chat(mess):
    chat_id = mess.chat.id
    mess_text = mess.text
    user_id = mess.chat.id
    if mess_text == 'PDF':
        try:
            file_list = os.listdir(f'temp_images/{chat_id}')
        except:
            bot.send_message(chat_id=chat_id, text='No haz enviado ninguna imagen')
            return 0
        if len(file_list) == 0:
            bot.send_message(chat_id=chat_id, text='No ha cargado images para convertir, primero envia las imagenes')
        else:
            mess1 = bot.send_message(chat_id=chat_id, text=f'Convirtiendo las imagenes a PDF')
            imgs_to_pdf(f'temp_images/{chat_id}',str(chat_id)+'gs')
            compress(f'{chat_id}gs.pdf',f'{chat_id}gsa.pdf', 0)
            bot.delete_message(chat_id=chat_id, message_id=mess1.message_id)
            mess2 = bot.send_message(chat_id=chat_id, text='Enviando archivo')
            with open(f'{chat_id}gsa.pdf', 'rb') as document:
                bot.send_document(chat_id=chat_id, document=document)
            bot.delete_message(chat_id=chat_id,message_id=mess2.message_id)
            try:
                user_actions[user_id] = None
                os.remove(f'{chat_id}gsa.pdf')
                os.remove(f'{chat_id}gs.pdf')
                shutil.rmtree(f'temp_images/{str(chat_id)}/')
                bot.send_message(chat_id=chat_id, text=f'Accion terminada', reply_markup=types.ReplyKeyboardRemove())
            except:
                bot.send_message(chat_id=chat_id, text=f'Accion terminada', reply_markup=types.ReplyKeyboardRemove())

    elif mess_text == 'Salir':
        try:
            user_actions[user_id] = None
            shutil.rmtree(f'temp_images/{str(chat_id)}/')
            bot.send_message(chat_id=chat_id, text=f'Saliendo de la accion', reply_markup=types.ReplyKeyboardRemove())
        except:
            bot.send_message(chat_id=chat_id, text=f'Saliendo de la accion', reply_markup=types.ReplyKeyboardRemove())
# Esto mantiene el bot ejecutandoce 
bot.infinity_polling()

