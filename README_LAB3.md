# Lab 3 — Automatización, Monitoreo y Contenerización

Archivos principales implementados:
- `backup_db.sh` — Genera backups comprimidos en `Backups/` y limpia antiguos.
- `resource_monitor.sh` — Monitoriza RAM y disco; imprime alertas si supera umbrales.
- `log_analyzer_blacklist.py` — Analiza `Server.log` en busca de patrones de ataque y agrega IPs a `ip_blacklist.txt`.
- `health_check.py` — Comprueba memoria, disco, backups y presencia de DB; función `run_all_checks()`.
- `Dockerfile`, `Dockerfile.dev`, `docker-compose.yml`, `deploy.sh` — Contenerización y despliegue.

Cómo ejecutar pruebas rápidas:

1. Scripts locales:

```bash
# Crear directorios necesarios
mkdir -p Backups data

# Ejecutar backup manual
bash backup_db.sh

# Ejecutar monitor de recursos
bash resource_monitor.sh

# Analizar logs (si existe Server.log)
python3 log_analyzer_blacklist.py

# Ejecutar health check
python3 health_check.py
```

2. Con Docker Compose:

```bash
# Construir y levantar
docker compose up -d --build
# Parar
docker compose down
```

3. Usar deploy.sh para construir y ejecutar la imagen de producción:

```bash
bash deploy.sh
```

Notas:
- Ajusta umbrales y rutas según el entorno.
- `ip_blacklist.txt` y `Server.log` son pieza clave para el análisis de ataques.
