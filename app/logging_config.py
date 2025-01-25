from elasticsearch import Elasticsearch
import structlog

# Conectar con Elasticsearch
es = Elasticsearch("http://localhost:9200")

def log_security_event(event_type, username, ip, status, details=""):
    log_entry = {
        "event_type": event_type,
        "username": username,
        "ip": ip,
        "status": status,
        "details": details
    }
    es.index(index="security-logs", body=log_entry)
