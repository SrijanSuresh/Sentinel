import psutil
from prometheus_client import start_http_server, Gauge
# creating gauge with name and description
MEMORY_USAGE = Gauge('sentinel_memory_usage_mb', 'Current memory usage of the guarded process')
PROCESS_STATUS = Gauge('sentinel_process_running', '1 if running, 0 if dead')

def start_metric_server(port=8000):
    try:
        # we start a background thread that prometheus can talk to
        start_http_server(port, addr='0.0.0.0')
        print(f"Metrics server started on 0.0.0.0:{port}")
    except OSError:
        # If port 8000 is already in use, we just ignore it and move on
        print(f"Port {port} already in use. Skipping metrics server for this instance.")
