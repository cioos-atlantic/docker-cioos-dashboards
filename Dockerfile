# For more information, please refer to https://aka.ms/vscode-docker-python
FROM continuumio/anaconda3
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libgtk2.0-dev && \
    rm -rf /var/lib/apt/lists/*


# Install pip requirements
COPY requirements.txt .

RUN conda config --add channels conda-forge
RUN /opt/conda/bin/conda update --all --yes
RUN /opt/conda/bin/conda create --name dashboard --file requirements.txt
RUN activate dashboard

RUN pip install -r requirements.txt

EXPOSE 8050

WORKDIR /app
COPY . /app




# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "PDBcioos_june1.py"]
