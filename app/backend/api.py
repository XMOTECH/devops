#!/usr/bin/env python3
from flask import Flask, jsonify, request, Response
from datetime import datetime
import os
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Gauge

app = Flask(__name__)

# Metriques Prometheus
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests', ['method', 'endpoint', 'http_status'])
HEALTH_CHECKS = Counter('app_health_checks_total', 'Total health checks performed', ['status'])
start_time = time.time()

# Stockage en mémoire (pour le lab)
health_checks = []

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route('/')
def home():
    return jsonify({
        "app": "DevOps Monitoring App",
        "version": "1.0.0",
        "status": "running",
        "hostname": os.getenv('HOSTNAME', 'unknown'),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Exercice 1: Endpoint Uptime
@app.route('/api/uptime')
def uptime():
    uptime_seconds = int(time.time() - start_time)
    return jsonify({
        "uptime_seconds": uptime_seconds,
        "start_time": datetime.fromtimestamp(start_time).isoformat()
    })

# Exercice 3: Endpoint Metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/api/checks', methods=['GET', 'POST'])
def checks():
    if request.method == 'POST':
        data = request.get_json()
        status_code = data.get("status")
        check = {
            "url": data.get("url"),
            "status": status_code,
            "timestamp": datetime.now().isoformat()
        }
        health_checks.append(check)
        
        # Increment metric
        status_label = 'success' if status_code == 200 else 'failure'
        HEALTH_CHECKS.labels(status=status_label).inc()
        
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