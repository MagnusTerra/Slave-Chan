import openai
import telebot
openai.api_key = "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"
bot = telebot.TeleBot("5471059094:AAG5dOnDrS0UPP_ysiaBNlNQBus45xfnnz0", parse_mode=None)

def openia(mess):
    completion = openai.Completion.create(engine="text-davinci-003", 
                                          prompt=mess,
                                          max_tokens= 2500)
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
