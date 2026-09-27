FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y ffmpeg

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
