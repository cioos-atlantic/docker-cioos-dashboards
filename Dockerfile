FROM continuumio/anaconda3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN apt-get update && apt-get install -y libgtk2.0-dev && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN conda config --add channels conda-forge
RUN /opt/conda/bin/conda update --all --yes
RUN /opt/conda/bin/conda create --name dashboard --file requirements.txt
RUN activate dashboard
RUN pip install -r requirements.txt
EXPOSE 8050
WORKDIR /app
COPY . /app
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn" "-b" "0.0.0.0:80" "/app/viz/app.py"]