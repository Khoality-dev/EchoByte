FROM python:3.10.17-slim-bullseye

RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
