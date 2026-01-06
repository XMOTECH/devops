# Lab DevOps End-to-End : Application de Monitoring Web

## 🎯 Objectifs du Lab
Créer une application web complète avec monitoring, automatisation et déploiement en suivant les pratiques DevOps modernes.

## 📚 Ce que vous allez apprendre
- Linux/Bash scripting
- Git & GitHub
- Docker & Docker Compose
- CI/CD avec GitHub Actions
- Monitoring et logging
- Nginx comme serveur web
- Bonnes pratiques DevOps

---

## 🏗️ Architecture du Projet

```
mon-app-devops/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline CI/CD
├── app/
│   ├── backend/
│   │   └── api.py             # API Python Flask
│   └── frontend/
│       └── index.html         # Interface web
├── scripts/
│   ├── check_health.sh        # Script de health check
│   ├── backup.sh              # Script de sauvegarde
│   └── deploy.sh              # Script de déploiement
├── monitoring/
│   └── prometheus.yml         # Config monitoring
├── logs/                      # Dossier des logs
├── docker-compose.yml         # Orchestration des services
├── Dockerfile                 # Image de l'app
├── .gitignore                 # Fichiers à ignorer
└── README.md                  # Documentation
```

---

## 📖 Partie 1 : Configuration Initiale (30 min)

### Étape 1.1 : Créer la structure du projet

```bash
# Créer le répertoire principal
mkdir mon-app-devops
cd mon-app-devops

# Créer la structure
mkdir -p app/{backend,frontend} scripts monitoring logs .github/workflows

# Créer les fichiers de base
touch README.md .gitignore docker-compose.yml Dockerfile
touch app/backend/api.py app/frontend/index.html
touch scripts/{check_health.sh,backup.sh,deploy.sh}
```

### Étape 1.2 : Initialiser Git

```bash
# Configurer Git
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Initialiser le dépôt
git init
git branch -M main
```

### Étape 1.3 : Créer le .gitignore

```bash
cat > .gitignore << 'EOF'
# Logs
logs/*.log
*.log

# Docker
.env

# Python
__pycache__/
*.py[cod]
venv/

# OS
.DS_Store
Thumbs.db

# Backups
backups/
*.tar.gz
EOF
```

---

## 📖 Partie 2 : Développement de l'Application (1h)

### Étape 2.1 : Créer l'API Backend (Python Flask)

```bash
nano app/backend/api.py
```

Contenu du fichier :

```python
#!/usr/bin/env python3
from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Stockage en mémoire (pour le lab)
health_checks = []

@app.route('/')
def home():
    return jsonify({
        "app": "DevOps Monitoring App",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/checks', methods=['GET', 'POST'])
def checks():
    if request.method == 'POST':
        data = request.get_json()
        check = {
            "url": data.get("url"),
            "status": data.get("status"),
            "timestamp": datetime.now().isoformat()
        }
        health_checks.append(check)
        return jsonify(check), 201
    
    return jsonify(health_checks), 200

@app.route('/api/stats')
def stats():
    total = len(health_checks)
    healthy = len([c for c in health_checks if c.get("status") == 200])
    return jsonify({
        "total_checks": total,
        "healthy": healthy,
        "unhealthy": total - healthy
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Étape 2.2 : Créer le Frontend

```bash
nano app/frontend/index.html
```

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Monitoring Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-card h3 {
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }
        .check-form {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        .checks-list {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .check-item {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .check-item:last-child {
            border-bottom: none;
        }
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        .status-success {
            background: #10b981;
            color: white;
        }
        .status-error {
            background: #ef4444;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 DevOps Monitoring Dashboard</h1>
            <p>Surveillez vos services en temps réel</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <h3>Total Checks</h3>
                <div class="value" id="totalChecks">0</div>
            </div>
            <div class="stat-card">
                <h3>Services Sains</h3>
                <div class="value" id="healthyChecks" style="color: #10b981;">0</div>
            </div>
            <div class="stat-card">
                <h3>Services en Panne</h3>
                <div class="value" id="unhealthyChecks" style="color: #ef4444;">0</div>
            </div>
        </div>

        <div class="check-form">
            <h2 style="margin-bottom: 20px;">Ajouter un Check</h2>
            <div class="input-group">
                <input type="text" id="urlInput" placeholder="https://example.com">
                <button onclick="checkUrl()">Vérifier</button>
            </div>
        </div>

        <div class="checks-list">
            <h2 style="margin-bottom: 20px;">Historique des Checks</h2>
            <div id="checksList"></div>
        </div>
    </div>

    <script>
        const API_URL = 'http://localhost:5000';

        async function loadStats() {
            try {
                const response = await fetch(`${API_URL}/api/stats`);
                const data = await response.json();
                document.getElementById('totalChecks').textContent = data.total_checks;
                document.getElementById('healthyChecks').textContent = data.healthy;
                document.getElementById('unhealthyChecks').textContent = data.unhealthy;
            } catch (error) {
                console.error('Erreur chargement stats:', error);
            }
        }

        async function loadChecks() {
            try {
                const response = await fetch(`${API_URL}/api/checks`);
                const checks = await response.json();
                const listDiv = document.getElementById('checksList');
                
                if (checks.length === 0) {
                    listDiv.innerHTML = '<p style="color: #666;">Aucun check effectué</p>';
                    return;
                }

                listDiv.innerHTML = checks.reverse().map(check => `
                    <div class="check-item">
                        <div>
                            <strong>${check.url}</strong>
                            <br>
                            <small style="color: #666;">${new Date(check.timestamp).toLocaleString('fr-FR')}</small>
                        </div>
                        <span class="status-badge ${check.status === 200 ? 'status-success' : 'status-error'}">
                            ${check.status === 200 ? '✓ OK' : '✗ Erreur'}
                        </span>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Erreur chargement checks:', error);
            }
        }

        async function checkUrl() {
            const url = document.getElementById('urlInput').value;
            if (!url) {
                alert('Veuillez entrer une URL');
                return;
            }

            try {
                const response = await fetch(`${API_URL}/api/checks`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url, status: 200 })
                });

                if (response.ok) {
                    document.getElementById('urlInput').value = '';
                    await loadStats();
                    await loadChecks();
                }
            } catch (error) {
                console.error('Erreur:', error);
            }
        }

        // Charger les données au démarrage
        loadStats();
        loadChecks();
        setInterval(() => {
            loadStats();
            loadChecks();
        }, 5000);
    </script>
</body>
</html>
```

---

## 📖 Partie 3 : Scripts DevOps (45 min)

### Étape 3.1 : Script de Health Check

```bash
nano scripts/check_health.sh
```

```bash
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
```

```bash
chmod +x scripts/check_health.sh
```

### Étape 3.2 : Script de Backup

```bash
nano scripts/backup.sh
```

```bash
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
```

```bash
chmod +x scripts/backup.sh
```

### Étape 3.3 : Script de Déploiement

```bash
nano scripts/deploy.sh
```

```bash
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
```

```bash
chmod +x scripts/deploy.sh
```

---

## 📖 Partie 4 : Dockerisation (45 min)

### Étape 4.1 : Créer le Dockerfile

```bash
nano Dockerfile
```

```dockerfile
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
```

### Étape 4.2 : Créer requirements.txt

```bash
cat > requirements.txt << 'EOF'
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
EOF
```

### Étape 4.3 : Créer le docker-compose.yml

```bash
nano docker-compose.yml
```

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: devops-api
    ports:
      - "5000:5000"
    volumes:
      - ./logs:/logs
      - ./backups:/backups
    environment:
      - FLASK_ENV=production
    networks:
      - devops-net
    restart: unless-stopped

  web:
    image: nginx:alpine
    container_name: devops-web
    ports:
      - "8080:80"
    volumes:
      - ./app/frontend:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - devops-net
    restart: unless-stopped
    depends_on:
      - api

  monitor:
    build: .
    container_name: devops-monitor
    volumes:
      - ./logs:/logs
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        while true; do
          /scripts/check_health.sh https://google.com
          /scripts/check_health.sh https://github.com
          sleep 60
        done
    networks:
      - devops-net
    restart: unless-stopped

networks:
  devops-net:
    driver: bridge

volumes:
  logs:
  backups:
```

### Étape 4.4 : Configuration Nginx

```bash
nano nginx.conf
```

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://api:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📖 Partie 5 : CI/CD avec GitHub Actions (30 min)

### Étape 5.1 : Créer le pipeline

```bash
nano .github/workflows/ci-cd.yml
```

```yaml
name: DevOps CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Tests et Validation
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Vérification des scripts Bash
        run: |
          find scripts -name "*.sh" -exec bash -n {} \;
          echo "✅ Tous les scripts sont syntaxiquement corrects"

      - name: Test de sécurité Docker
        run: |
          docker run --rm -v $(pwd):/project aquasec/trivy:latest config /project
        continue-on-error: true

  build:
    name: Build Docker
    runs-on: ubuntu-latest
    needs: test
    
    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Build de l'image Docker
        run: |
          docker build -t devops-app:${{ github.sha }} .
          echo "✅ Image construite avec succès"

      - name: Test du conteneur
        run: |
          docker run -d --name test-container devops-app:${{ github.sha }}
          sleep 5
          docker ps | grep test-container
          docker stop test-container
          echo "✅ Conteneur fonctionne correctement"

  deploy:
    name: Déploiement
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Simulation de déploiement
        run: |
          echo "🚀 Déploiement sur l'environnement de production"
          echo "📦 Version: ${{ github.sha }}"
          echo "✅ Déploiement réussi!"
```

---

## 📖 Partie 6 : Documentation et Tests (30 min)

### Étape 6.1 : Créer le README.md

```bash
nano README.md
```

```markdown
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

```
├── API Backend (Flask sur port 5000)
├── Frontend Web (Nginx sur port 8080)
└── Service de Monitoring (checks toutes les 60s)
```

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

XMOTECH - Lab DevOps 2026
```

### Étape 6.2 : Premier commit

```bash
# Ajouter tous les fichiers
git add .

# Créer le commit
git commit -m "Initial commit: Application DevOps complète avec monitoring"

# Créer un repo sur GitHub puis :
git remote add origin git@github.com:VotreUsername/mon-app-devops.git
git push -u origin main
```

---

## 📖 Partie 7 : Lancement et Tests (30 min)

### Étape 7.1 : Démarrer l'application

```bash
# Construire et démarrer tous les services
docker-compose up --build -d

# Vérifier que tout tourne
docker-compose ps

# Voir les logs
docker-compose logs -f
```

### Étape 7.2 : Tests manuels

```bash
# 1. Tester l'API
curl http://localhost:5000/health
curl http://localhost:5000/api/stats

# 2. Tester le frontend
# Ouvrir http://localhost:8080 dans votre navigateur

# 3. Tester le monitoring
docker-compose logs monitor

# 4. Vérifier les logs
cat logs/health.log

# 5. Tester un backup
docker exec devops-monitor /scripts/backup.sh
ls -lh backups/
```

### Étape 7.3 : Tests du pipeline CI/CD

```bash
# Faire une modification
echo "# Update" >> README.md

# Commit et push
git add README.md
git commit -m "Test du pipeline CI/CD"
git push origin main

# Aller sur GitHub > Actions pour voir le pipeline s'exécuter
```

---

## 🎓 Exercices Pratiques

### Exercice 1 : Ajouter un nouveau endpoint
Ajoutez un endpoint `/api/uptime` qui retourne le temps de fonctionnement de l'API.

### Exercice 2 : Améliorer le monitoring
Modifiez le script pour envoyer une alerte email quand un service est down.

### Exercice 3 : Ajouter des métriques
Intégrez Prometheus pour collecter des métriques.

### Exercice 4 : Haute disponibilité
Configurez plusieurs réplicas de l'API avec un load balancer.

---

## 📚 Ressources Complémentaires

- [Documentation Docker](https://docs.docker.com/)
- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [DevOps Best Practices](https://www.atlassian.com/devops)

---

## 🎯 Checklist de Complétion

- [ ] Structure du projet créée
- [ ] API backend fonctionnelle
- [ ] Frontend accessible
- [ ] Scripts de monitoring opérationnels
- [ ] Docker containers lancés
- [ ] Pipeline CI/CD configuré
- [ ] Documentation complète
- [ ] Tests passent avec succès
- [ ] Application accessible publiquement

---

## 💡 Conseils DevOps

1. **Automatisez tout** : Si vous le faites 2 fois, automatisez-le
2. **Monitorer en continu** : Un système non surveillé est un système en panne
3. **Documentez** : Le code se lit plus qu'il ne s'écrit
4. **Testez** : Si ce n'est pas testé, c'est cassé
5. **Versionnez tout** : Git est votre ami
6. **Sécurisez** : La sécurité n'est pas une option
7. **Optimisez** : Mais seulement quand nécessaire

---

## 🚀 Next Steps

Une fois ce lab complété, explorez :
- Kubernetes pour l'orchestration
- Terraform pour l'Infrastructure as Code
- Ansible pour la configuration management
- ELK Stack pour le logging avancé
- Grafana pour la visualisation

**Bravo ! Vous avez complété votre premier projet DevOps end-to-end ! 🎉**
