# ══════════════════════════════════════════════════════════════════════════════
# FinTech Nova — Motor de Riesgo Crediticio
# API desarrollada con FastAPI para evaluación de solicitudes de crédito
# Laboratorio 1: Despliegue Base y Arquitectura
# ══════════════════════════════════════════════════════════════════════════════

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from health_check import run_all_checks

# ── CONFIGURACIÓN DE LA APLICACIÓN ───────────────────────────────────────────
app = FastAPI(
    title="FinTech Nova - Motor de Riesgo",
    version="1.0.0",
    description="API para evaluación de riesgo crediticio"
)

@app.get("/")
def read_root():
    return {
        "mensaje": "FinTech Nova API está en línea",
        "endpoints": ["/status", "/evaluar-riesgo", "/datos-financieros/{id}"]
    }

# ── MODELO DE DATOS — SOLICITUD DE CRÉDITO ──────────────────────────────────
# Esta clase define la estructura que espera recibir el endpoint POST /evaluar-riesgo
# FastAPI usa Pydantic para validar automáticamente que los datos cumplan este formato
class SolicitudCredito(BaseModel):
    edad: int          # Edad del solicitante (debe ser número entero)
    ingresos: float    # Ingresos mensuales (debe ser número decimal)
    deudas: float      # Deudas mensuales (debe ser número decimal)


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 1: GET /status
# ══════════════════════════════════════════════════════════════════════════════
@app.get("/status")
def get_status():
    """
    Health Check — Verifica que el motor de riesgo está operativo.
    
    Usado por: Sistemas de monitoreo (Lab 3)
    Retorna: Estado del servidor y información de salud
    
    Ejemplo de respuesta:
    {
        "estado": "Operacional",
        "servidor": "Nodo-01"
    }
    """
    return {
        "estado": "Operacional",
        "servidor": "Nodo-01"
    }


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 2: POST /evaluar-riesgo
# ══════════════════════════════════════════════════════════════════════════════
@app.post("/evaluar-riesgo")
def evaluar_riesgo(solicitud: SolicitudCredito):
    """
    Motor de Evaluación de Riesgo Crediticio.
    
    Recibe: Datos de solicitud (edad, ingresos, deudas)
    Retorna: Decisión (Aprobado / En Revisión / Rechazado) + score calculado
    
    Usado por: App móvil del cliente
    
    Reglas de negocio:
    1. Menores de 18 años: RECHAZADO (requisito legal)
    2. Score > 1000: APROBADO (ingresos sanos sobre deudas)
    3. Otros casos: EN REVISIÓN (requiere análisis humano)
    
    Ejemplo de entrada:
    {
        "edad": 25,
        "ingresos": 3000.0,
        "deudas": 500.0
    }
    """
    
    # ─ LÓGICA DE NEGOCIO ────────────────────────────────────────────────────
    # Score = Diferencia entre ingresos y deudas mensuales
    # En producción, esto sería un modelo de ML completo
    score = solicitud.ingresos - solicitud.deudas
    
    # Regla 1: Menores de edad siempre rechazados (requisito legal)
    if solicitud.edad < 18:
        resultado = "Rechazado (Menor de edad)"
    
    # Regla 2: Score positivo mayor a 1000 = ingresos sanos sobre deudas
    elif score > 1000:
        resultado = "Aprobado"
    
    # Regla 3: Cualquier otro caso requiere revisión manual
    else:
        resultado = "En Revision"
    
    # Retornamos el resultado y el score para auditoría
    return {
        "resultado": resultado,
        "score_simulado": score
    }


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 3: GET /datos-financieros/{id_cliente}
# ══════════════════════════════════════════════════════════════════════════════
@app.get("/datos-financieros/{id_cliente}")
def obtener_historial(id_cliente: int):
    """
    Consulta de Historial Financiero por ID.
    
    ⚠️ VULNERABILIDAD INTENCIONAL (se corrige en Lab 2)
    
    Este endpoint NO verifica autenticación ni autorización.
    Cualquier persona con la URL puede obtener datos de CUALQUIER cliente.
    
    En producción real, esto es una violación a regulaciones como:
    - Habeas Data (Colombia): multas hasta 2000 SMLMV
    - GDPR (Europa): multas hasta €20 millones
    - CCPA (USA): privacidad de datos del consumidor
    
    Usado por: Sistema interno (sin protección en Lab 1)
    
    En Lab 2: Se añadirá autenticación JWT para proteger este endpoint
    
    Parámetro:
    - id_cliente: int (ejemplo: GET /datos-financieros/42)
    """
    return {
        "cliente_id": id_cliente,
        "historial": "Limpio",
        "score_interno": 750
    }


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 4: GET /health
# ══════════════════════════════════════════════════════════════════════════════
@app.get("/health")
def get_health():
    """
    Health Check completo para Lab 3.

    Verifica memoria, disco, backups y estado de la base de datos.
    Retorna: estado general y detalles de cada verificación.
    """
    return run_all_checks()