web: web: gunicorn dmlsite.wsgi:application
web2: daphne dmlsite.asgi:application --port $port --bind 0.0.0.0 -v2
worker: python workers.py
