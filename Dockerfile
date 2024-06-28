FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install requests
RUN pip install flask

CMD ["python", "app/app.py"]