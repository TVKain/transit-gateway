FROM python:3.10.14-slim

WORKDIR /app

COPY ./app /app
COPY requirements.txt /app

RUN pip install -r requirements.txt 

EXPOSE 8000

WORKDIR /

CMD ["fastapi", "dev"]