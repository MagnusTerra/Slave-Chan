# Importamos las librerias necesarias 
import cv2
import pytesseract

# Definimos una función para realizar el reconocimiento óptico de caracteres (OCR) horizontal
# Recibe la ruta de la imagen a procesar como parámetro
def ocr_horizontal(image_path):
    # Cargamos la imagen en escala de grises usando la librería cv2
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) 
    
    # Aplicamos un umbral para eliminar el ruido y mejorar la calidad de la imagen
    threshold_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Utilizamos la librería pytesseract para obtener el texto de la imagen procesada
    text = pytesseract.image_to_string(threshold_img, config='--psm 3')

    # Devolvemos el texto obtenido
    return text



