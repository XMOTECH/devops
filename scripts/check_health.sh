#!/bin/bash

URL="${1:-https://google.com}"
LOG_FILE="/logs/health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Créer le dossier logs s'il n'existe pas
mkdir -p /logs

# Effectuer le check avec suivi des redirections
HTTP_CODE=$(curl -L -o /dev/null -s -w "%{http_code}" --max-time 10 "$URL")

if [ "$HTTP_CODE" = "200" ]; then
    echo "[$TIMESTAMP] ✅ [OK] $URL (Code: $HTTP_CODE)" | tee -a "$LOG_FILE"
    exit 0
else
    echo "[$TIMESTAMP] ❌ [ERREUR] $URL (Code: $HTTP_CODE)" | tee -a "$LOG_FILE"
    exit 1
fi