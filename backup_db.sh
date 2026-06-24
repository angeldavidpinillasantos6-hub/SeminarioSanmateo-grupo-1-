#!/usr/bin/env bash
set -euo pipefail

# Directorio de backups
BACKUP_DIR="Backups"
mkdir -p "$BACKUP_DIR"

# Nombre base de la BD (si existe), por defecto copia archivos .sqlite en data/
DB_SOURCE_DIR="data"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUT_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.tar.gz"

# Incluir archivos de la carpeta data si existen
if [ -d "$DB_SOURCE_DIR" ] && [ "$(ls -A $DB_SOURCE_DIR)" ]; then
  tar -czf "$OUT_FILE" -C "$DB_SOURCE_DIR" .
else
  # Si no hay data, creamos un backup mínimo con metadatos
  echo "No hay archivos en $DB_SOURCE_DIR. Generando backup vacío con timestamp" > /tmp/backup_info.txt
  tar -czf "$OUT_FILE" -C /tmp backup_info.txt
  rm /tmp/backup_info.txt
fi

# Limpiar backups antiguos: conservar 7 días
find "$BACKUP_DIR" -type f -mtime +7 -name "backup_*.tar.gz" -delete

echo "Created backup: $OUT_FILE"
