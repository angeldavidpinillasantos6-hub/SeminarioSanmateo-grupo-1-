# Production Dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Use non-root user
USER appuser

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD ["/usr/bin/python","-c","import requests,sys; r=requests.get('http://127.0.0.1:8000/health'); sys.exit(0 if r.status_code==200 else 1)"]

CMD ["/usr/local/bin/uvicorn","main:app","--host","0.0.0.0","--port","8000"]
