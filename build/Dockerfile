FROM python:3.12-slim

WORKDIR /app

COPY .. .

RUN pip3 install -r requirements.txt

WORKDIR /app/src

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "9100", "app.py"]