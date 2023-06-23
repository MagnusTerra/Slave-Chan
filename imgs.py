# Importamos la librería PIL
from PIL import Image

# Función que convierte una imagen en formato .jpg a .png
def conver_img(img, name):
  img = Image.open(img) # Abrimos la imagen con PIL
  img.save(f'{name}.png', 'png') # Guardamos la imagen en formato .png

# Función que redimensiona una imagen a 512px de ancho y alto
def resize_img(img, name):
  img = Image.open(img)
  new_width = 512 # Definimos el ancho que queremos para la imagen redimensionada
  new_height = 512 # Calculamos el alto proporcional al ancho nuevo
  img = img.resize((new_width, new_height)) # Redimensionamos la imagen con PIL

  img.save(f'{name}.png', 'png') # Guardamos la imagen redimensionada en formato .png
