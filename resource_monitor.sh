#!/usr/bin/env bash
# Monitorea uso de RAM y disco, imprime advertencia si supera umbrales

RAM_THRESHOLD=80
DISK_THRESHOLD=85

# Obtener uso de memoria (porcentaje usado)
RAM_USED=$(free -m | awk '/^Mem:/ {printf("%d", $3/$2 * 100)}')
# Obtener uso de disco del root
DISK_USED=$(df --output=pcent / | tail -1 | tr -dc '0-9')

echo "RAM used: ${RAM_USED}%"
echo "Disk used: ${DISK_USED}%"

if [ "$RAM_USED" -ge "$RAM_THRESHOLD" ]; then
  echo "ALERTA: Uso de RAM >= ${RAM_THRESHOLD}%" >&2
fi

if [ "$DISK_USED" -ge "$DISK_THRESHOLD" ]; then
  echo "ALERTA: Uso de Disco >= ${DISK_THRESHOLD}%" >&2
fi

# Resumen
cat <<EOF
Resumen de recursos:
- RAM: ${RAM_USED}%
- Disco: ${DISK_USED}%
EOF
