FROM python:3.11-alpine

WORKDIR /app

# Installer les dépendances système
RUN apk add --no-cache curl bash

# Copier les requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY app/backend/ .
COPY scripts/ /scripts/

# Créer le dossier logs
RUN mkdir -p /logs

# Rendre les scripts exécutables
RUN chmod +x /scripts/*.sh

EXPOSE 5000

CMD ["python", "api.py"]