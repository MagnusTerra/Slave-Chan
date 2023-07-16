from telebot import types

def pdf_buttons():
    markup = types.ReplyKeyboardMarkup(True)
    markup.row('PDF', 'Salir')
    return markup