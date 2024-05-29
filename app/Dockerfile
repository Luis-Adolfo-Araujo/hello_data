# app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Copiar o arquivo requirements.txt do diretório raiz do projeto
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0"]
