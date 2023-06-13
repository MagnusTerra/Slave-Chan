# Importamos las librerias necesarias 
import cv2
import pytesseract

def ocr_horizontal(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) #Cargamos la imagen usando la libreria cv2
    
    threshold_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(threshold_img, config='--psm 3')

    return text


