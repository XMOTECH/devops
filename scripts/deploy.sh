#!/bin/bash

echo "🚀 Déploiement de l'application..."

# Arrêter les conteneurs existants
echo "📦 Arrêt des conteneurs..."
docker-compose down

# Reconstruire les images
echo "🔨 Construction des images..."
docker-compose build

# Démarrer les services
echo "▶️  Démarrage des services..."
docker-compose up -d

# Vérifier le statut
echo "✅ Services démarrés avec succès!"
docker-compose ps
