# Usa la imagen base de Ubuntu
FROM ubuntu:latest

# Actualiza el sistema y instala las dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    tesseract-ocr

RUN pip3 install requirements.txt

RUN python3 main.py