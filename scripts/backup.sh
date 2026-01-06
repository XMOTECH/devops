#!/bin/bash

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
LOGS_DIR="/logs"

mkdir -p "$BACKUP_DIR"

echo "🔄 Création du backup $DATE..."
tar -czf "$BACKUP_DIR/logs_backup_$DATE.tar.gz" -C / logs/

echo "✅ Backup créé : logs_backup_$DATE.tar.gz"

# Garder seulement les 5 derniers backups
ls -t "$BACKUP_DIR"/logs_backup_*.tar.gz | tail -n +6 | xargs -r rm

echo "🧹 Anciens backups nettoyés"