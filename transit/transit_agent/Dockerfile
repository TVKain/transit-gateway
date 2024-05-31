FROM python:3.10.14-slim

WORKDIR /app

COPY . /app
COPY requirements.txt /app

RUN pip install -r requirements.txt 

EXPOSE 3000

WORKDIR /

CMD ["python", "-m",  "app.run"]