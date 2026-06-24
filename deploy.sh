#!/usr/bin/env bash
set -euo pipefail

# Verificar Docker
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker no está instalado" >&2
  exit 1
fi

IMAGE_NAME="fintech-nova:1.0"
CONTAINER_NAME="fintech-nova-app"

# Construir imagen
docker build -t $IMAGE_NAME .

# Detener y eliminar contenedor anterior si existe
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker rm -f ${CONTAINER_NAME}
fi

# Ejecutar contenedor
docker run -d --name ${CONTAINER_NAME} -p 8000:8000 -v $(pwd)/Backups:/app/Backups $IMAGE_NAME

# Esperar inicio
sleep 3

# Verificar /health
if curl -sS http://localhost:8000/health | grep -q '"status"'; then
  echo "Despliegue confirmado. /health disponible"
else
  echo "Despliegue falló o /health no responde" >&2
  docker logs ${CONTAINER_NAME}
  exit 2
fi
