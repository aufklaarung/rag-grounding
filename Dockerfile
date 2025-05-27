# Utilise une image officielle Python
FROM python:3.11-slim AS builder

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=True

RUN apt-get update \
  && apt-get install gcc -y \
  && apt-get clean

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

# Définir le répertoire de travail
WORKDIR /code

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-root

# Copier les fichiers nécessaires
COPY src src
COPY chroma chroma
COPY templates templates
COPY static static
COPY app.py .
COPY .env .

#Expose le port
EXPOSE 8080

# Commande de lancement
ENTRYPOINT ["python", "app.py"]