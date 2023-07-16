FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    tesseract-ocr \
    libgl1-mesa-glx \
    ghostscript


COPY requirements.txt .

COPY install.sh .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x /install.sh

RUN /install.sh

COPY . .
