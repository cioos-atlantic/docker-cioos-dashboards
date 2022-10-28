FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN apt-get update && apt-get install -y libgtk2.0-dev && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8050
WORKDIR /app
COPY . /app
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD gunicorn --chdir viz -b 0.0.0.0:8050 app:server