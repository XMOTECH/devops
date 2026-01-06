# 🚀 Application DevOps de Monitoring

Application de monitoring web complète avec CI/CD, containerisation et scripts automatisés.

## 🎯 Fonctionnalités

- ✅ API REST en Python/Flask
- 🌐 Dashboard web interactif
- 🔍 Monitoring automatique des services
- 📊 Statistiques en temps réel
- 🐳 Containerisation avec Docker
- 🔄 CI/CD avec GitHub Actions
- 📝 Logging complet
- 💾 Système de backup automatique

## 🏗️ Architecture
## 🚀 Installation

### Prérequis
- Docker & Docker Compose
- Git

### Lancement rapide
```bash
# Cloner le projet
git clone <votre-repo>
cd mon-app-devops

# Démarrer l'application
docker-compose up -d

# Vérifier les services
docker-compose ps
```

## 📖 Utilisation

### Accéder à l'application
- **Frontend**: http://localhost:8080
- **API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

### Commandes utiles
```bash
# Voir les logs
docker-compose logs -f

# Arrêter l'application
docker-compose down

# Reconstruire les images
docker-compose build

# Créer un backup
docker exec devops-monitor /scripts/backup.sh

# Check manuel d'un site
docker exec devops-monitor /scripts/check_health.sh https://example.com
```

## 🧪 Tests
```bash
# Test de l'API
curl http://localhost:5000/health

# Test du frontend
curl http://localhost:8080

# Test des scripts
./scripts/check_health.sh https://google.com
```

## 📊 Monitoring

Les logs sont stockés dans `./logs/health.log`
```bash
# Voir les logs en temps réel
tail -f logs/health.log

# Voir les statistiques
curl http://localhost:5000/api/stats
```

## 🔧 Configuration

Modifier le fichier `docker-compose.yml` pour ajuster :
- Les ports exposés
- Les intervalles de monitoring
- Les sites à surveiller

## 📦 Déploiement

Le pipeline CI/CD se déclenche automatiquement à chaque push sur `main`.

Étapes :
1. ✅ Tests des scripts
2. 🔨 Build Docker
3. 🧪 Tests du conteneur
4. 🚀 Déploiement

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push sur la branche (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

## 📝 License

MIT

## 👤 Auteur

XMOTECH - Lab DevOps 2026# Update
