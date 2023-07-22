from telebot import types
import os
import sys
import subprocess
import cv2
import pytesseract
import requests
import shutil
import img2pdf
import openai
import telebot
from PIL import Image
try:
    bot_token = os.environ['TOKEN']
    bot = telebot.TeleBot(bot_token, parse_mode=None)
except:
    pass
try:
    openaiKey = os.environ['KEY']
    openai.api_key = openaiKey
except:
    pass


class SLPDF:
    '''
    Esta Clase es para convertir imagenes a un PDF y reducirlo por si el archivo 
    es muy grande.

    ----------------------------------------------------------------
    Parámetros:
    dire: Es la ruta de la carpeta donde se encuentran las imagenes
    name: Es el nombre del PDF
    '''
    def __init__(self, dire, name, poten = 0):
        
        self.name = name
        self.impdf = self.imgs_to_pdf(dire, f'{self.name}gs')
        self.pdf_compress = self.compress(f'{self.name}gs.pdf', f'{self.name}gsa.pdf', poten)
        
    def imgs_to_pdf(self, carpeta, name):
        imagenes = []

        # Obtener todas las imágenes de la carpeta
        archivos = os.listdir(carpeta)
        archivos_ordenados = sorted(archivos, key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else float('inf'))

        for archivo in archivos_ordenados:
            if archivo.endswith(".webp") or archivo.endswith(".jpg") or archivo.endswith(".png"):
                imagenes.append(os.path.join(carpeta, archivo))

        # Crear el archivo PDF
        with open(f'{name}.pdf', "wb") as pdf:
            pdf.write(img2pdf.convert(imagenes))

    @classmethod
    def compress(self, input_file_path, output_file_path, power=0):
        """Función para comprimir PDF via Ghostscript """
        quality = {
            0: '/default',
            1: '/prepress',
            2: '/printer',
            3: '/ebook',
            4: '/screen'
        }

        # Comprovamos si existe el fichero
        if not os.path.isfile(input_file_path):
            print("Error: invalid path for input PDF file")
            sys.exit(1)

        # Comprobamos si es un pdf
        if input_file_path.split('.')[-1].lower() != 'pdf':
            print("Error: input file is not a PDF")
            sys.exit(1)

        gs = self.get_ghostscript_path()
        print("Compress PDF...")
        initial_size = os.path.getsize(input_file_path)
        subprocess.call([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                        '-dPDFSETTINGS={}'.format(quality[power]),
                        '-dNOPAUSE', '-dQUIET', '-dBATCH',
                        '-sOutputFile={}'.format(output_file_path),
                        input_file_path]
                        )
        final_size = os.path.getsize(output_file_path)
        ratio = 1 - (final_size / initial_size)
        resul1 = "Initial Size: {0:.1f}MB".format(initial_size / 1000000)
        resul2 = "Compression by {0:.0%}.".format(ratio)
        resul3 = "Final file size is {0:.1f}MB".format(final_size / 1000000)
        result = f'{resul1}\n{resul2}\n{resul3}\nPoder: {power}\nDone'
        return result

    @classmethod
    def get_ghostscript_path(self):
        gs_names = ['gs', 'gswin32', 'gswin64']
        for name in gs_names:
            if shutil.which(name):
                return shutil.which(name)
        raise FileNotFoundError(f'No GhostScript executable was found on path ({"/".join(gs_names)})')

#----------------------------------------------------------------   
 
class SLImage:
  def __init__(self):
    pass
  
  def convert_to_png(img: str, name: str = None, out_dir: str = None):
        '''Esta funcion convierte una img a png'''
        if out_dir is None: out_dir = './'
        if name is None:
            name = '\n'.join(img.split('/')[-1].rsplit('.', 1)[:-1])
            #print(name)
        try:
            img = Image.open(img)
            img.save(f'{out_dir}/{name}.png', 'png')
        except OSError as e:
            print( f'Error {img}: {e}')
            return f'Error {img}: {e}'
        
  def resize_img(img: str, name: str = None, new_width: int = None, new_height: int = None, out_dir: str = None):
    if new_width is None: new_width = 512
    if new_height is None: new_height = 512
    if out_dir is None: out_dir = './'
    if name is None: 
        name = '\n'.join(img.split('/')[-1].rsplit('.', 1)[:-1])
    img = Image.open(img)
    img = img.resize((new_width, new_height))
    path_file = f'{out_dir}/{name}resize.png'
    img.save(path_file, 'png') 
    return path_file

class SLOCR:

    def __init__(self, image_path: str, source_lang: str = None, target_lang: str=None):
        self.image_path = image_path
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.ocr = self.ocr_horizontal(self.image_path)
        

    # Función para realizar el reconocimiento óptico de caracteres (OCR) horizontal
    def ocr_horizontal(self, image_path):
        # Cargamos la imagen en escala de grises usando la librería cv2
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) 
        
        # Aplicamos un umbral para eliminar el ruido y mejorar la calidad de la imagen
        threshold_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Utilizamos la librería pytesseract para obtener el texto de la imagen procesada
        text = pytesseract.image_to_string(threshold_img, config='--psm 3')

        # Devolvemos el texto obtenido
        return text
    
    @classmethod
    def translate(self, text: str, source_lang, target_lang):
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format(
            source_lang, target_lang, text
        )
        response = requests.get(url)
        response_data = response.json()

        translation = ""
        if len(response_data) > 0 and isinstance(response_data[0], list):
            for item in response_data[0]:
                if item[0]:
                    translation += item[0]

        return translation

    def tostrn(self):
        if self.source_lang is not None and self.target_lang is not None:
            translated_text = self.translate(self.ocr, self.source_lang, self.target_lang)
            return translated_text
        else:
            return self.ocr



# functions without classes 
def pdf_buttons():
    markup = types.ReplyKeyboardMarkup(True)
    markup.row('PDF', 'Salir')
    return markup

def openia(mess):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": mess}])
    return str(completion.choices[0].message.content)


def openimage(mess):
    image_resp = openai.Image.create(prompt=mess, n=2, size="1024x1024")
    image_url = image_resp['data'][0]['url']
    return str(image_url)

def download_image(image, cid, path: str=None):
    if path is None: path = './'
    # Obtener la información de la foto
    photo_id = image.photo[-1].file_id
    photo_info = bot.get_file(photo_id)
    file_path = photo_info.file_path
    # Nombre del archivo y descarga del archivo a local
    file_name = f"{cid}.jpg"
    file = bot.download_file(file_path)
    path_file = f'{path}/{file_name}'  

    with open(path_file, "wb") as photo:
        photo.write(file)
    
    return path_file