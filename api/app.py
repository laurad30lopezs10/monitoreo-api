from flask import Flask, Response
import time
import random
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import psutil

app = Flask(__name__)

# Métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Latency', ['endpoint'])
ACTIVE_REQUESTS = Gauge('active_requests', 'Active requests')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage')

@app.before_request
def before():
    ACTIVE_REQUESTS.inc()

@app.after_request
def after(response):
    ACTIVE_REQUESTS.dec()
    return response

@app.route('/')
def home():
    REQUEST_COUNT.labels(endpoint='/').inc()
    return "API funcionando"

@app.route('/api/datos')
def datos():
    start = time.time()
    REQUEST_COUNT.labels(endpoint='/api/datos').inc()

    data = {"valor": random.randint(1, 100)}

    REQUEST_LATENCY.labels(endpoint='/api/datos').observe(time.time() - start)
    return data

@app.route('/api/lento')
def lento():
    start = time.time()
    REQUEST_COUNT.labels(endpoint='/api/lento').inc()

    time.sleep(3)

    REQUEST_LATENCY.labels(endpoint='/api/lento').observe(time.time() - start)
    return {"mensaje": "respuesta lenta"}

@app.route('/metrics')
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)