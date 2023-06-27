import os
import img2pdf
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
    
# Ejemplo de uso
def reduce_pdf_size(pdf):
    reader = PdfReader(pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(reader.metadata)

    with open(f"{pdf}_decude.pdf", "wb") as fp:
        writer.write(fp)