import os
import img2pdf
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter

def imgs_to_pdf(carpeta, name):
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
    
def imgs_to_pdf2(carpeta, name):
    imagenes = []

    # Obtener todas las imágenes de la carpeta
    archivos = os.listdir(carpeta)
    archivos_ordenados = sorted(archivos)

    for archivo in archivos_ordenados:
        if archivo.endswith(".webp") or archivo.endswith(".jpg") or archivo.endswith(".png"):
            imagenes.append(os.path.join(carpeta, archivo))

    # Crear el archivo PDF
    with open(f'{name}.pdf', "wb") as pdf:
        pdf.write(img2pdf.convert(imagenes))

# Ejemplo de uso
def reduce_pdf_size(pdf):
    with open(pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages) ):
            page = reader.pages[page_num]
            page.compress_content_streams()  # Comprimir el contenido de la página
            writer.add_page(page)

        with open(f'{pdf}_decude.pdf', 'wb') as output_file:
            writer.write(output_file)