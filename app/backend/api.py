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