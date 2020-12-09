FROM python:3.6

COPY src/ /app/

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ENV PORT 8080

ENV TORCH_HOME /app/models

RUN python3 model_yukle.py

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app