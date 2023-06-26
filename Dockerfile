FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    tesseract-ocr \
    libgl1-mesa-glx \
    aria2

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]
