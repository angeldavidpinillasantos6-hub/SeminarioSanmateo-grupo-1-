# FinTech Nova — Motor de Riesgo Crediticio

> API de evaluación de créditos — Roslaysoft Consulting  
> Laboratorio 1: Despliegue Base y Arquitectura

---

## 👥 Integrantes del Grupo

- Juan Felipe Pinilla Santos
- Ronald Perez Vargas
- Sara Marcela Rivera Mendoza

---

## 📊 Laboratorio 1 — Estado: COMPLETADO ✅

### 🌐 URL del Codespace
[Insertar aquí la URL pública del Codespace con la API corriendo]

---

## 🔌 Endpoints Disponibles

| Endpoint | Método | Descripción | Estado |
|----------|--------|-------------|--------|
| `/status` | GET | Health check del sistema | ✅ Operacional |
| `/evaluar-riesgo` | POST | Motor de scoring crediticio | ✅ Funcionando |
| `/datos-financieros/{id}` | GET | Historial financiero (VULNERABLE) | ⚠️ Sin autenticación |

### 📋 Detalles por Endpoint

#### 1. GET `/status`
**Propósito:** Verificar que el motor de riesgo está operativo  
**Usado por:** Sistemas de monitoreo (Lab 3)  
**Respuesta exitosa:**
```json
{
  "estado": "Operacional",
  "servidor": "Nodo-01"
}
```

#### 2. POST `/evaluar-riesgo`
**Propósito:** Recibir datos del solicitante y devolver decisión de crédito  
**Usado por:** App móvil del cliente  
**Body esperado:**
```json
{
  "edad": 25,
  "ingresos": 3000.0,
  "deudas": 500.0
}
```
**Respuesta exitosa:**
```json
{
  "resultado": "Aprobado",
  "score_simulado": 2500
}
```

#### 3. GET `/datos-financieros/{id}`
**Propósito:** Consultar historial crediticio de un cliente  
**⚠️ VULNERABILIDAD:** Sin autenticación (se protege en Lab 2)  
**Usado por:** Sistema interno  
**Respuesta:**
```json
{
  "cliente_id": 42,
  "historial": "Limpio",
  "score_interno": 750
}
```

---

## 🏗️ Diagrama Arquitectónico As-Is

![Arquitectura As-Is Lab 1](docs/diagramas/arquitectura_as_is_lab1.png)

**Componentes:**
- **Cliente:** App Móvil / Navegador
- **Internet:** Conexión HTTPS / Red Pública
- **Servidor:** GitHub Codespaces (Microsoft Azure)
  - Contenedor Linux Efímero
  - FastAPI + Uvicorn (Puerto 8000)
  - 3 endpoints con protección progresiva

---

## 🚀 Cómo Ejecutar

### 1. Clonar el repositorio
```bash
git clone https://github.com/RoslayBautista/SeminarioSanmateo.git
cd SeminarioSanmateo-grupo-1-
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar el servidor
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Acceder a la API
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **API Base:** http://localhost:8000

---

## 🧪 Casos de Prueba

### Prueba 1: Solicitud Aprobada
```bash
curl -X POST "http://localhost:8000/evaluar-riesgo" \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 25,
    "ingresos": 3000,
    "deudas": 500
  }'
```
**Resultado esperado:** `"resultado": "Aprobado"`

### Prueba 2: Solicitud en Revisión
```bash
curl -X POST "http://localhost:8000/evaluar-riesgo" \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 28,
    "ingresos": 2000,
    "deudas": 1000
  }'
```
**Resultado esperado:** `"resultado": "En Revision"`

### Prueba 3: Solicitud Rechazada (Menor)
```bash
curl -X POST "http://localhost:8000/evaluar-riesgo" \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 16,
    "ingresos": 1000,
    "deudas": 500
  }'
```
**Resultado esperado:** `"resultado": "Rechazado (Menor de edad)"`

### Prueba 4: Verificar Status
```bash
curl -X GET "http://localhost:8000/status"
```

---

## 📁 Estructura del Proyecto

```
SeminarioSanmateo-grupo-1-/
├── main.py                          # Código principal de la API
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Este archivo
├── docs/
│   └── diagramas/
│       └── arquitectura_as_is_lab1.png  # Diagrama arquitectónico
└── .git/                            # Control de versiones
```

---

## 📚 Dependencias

- **Python:** 3.9+
- **FastAPI:** Framework web moderno y rápido
- **Uvicorn:** Servidor ASGI (ejecutor de FastAPI)
- **Pydantic:** Validación de datos automática

---

## ⚠️ Vulnerabilidades Conocidas (Por Diseño)

### Lab 1 — Endpoint sin autenticación
- `/datos-financieros/{id}` no verifica credenciales
- **Riesgo:** Exposición de datos confidenciales
- **Regulaciones afectadas:** Habeas Data (Colombia), GDPR (Europa), CCPA (USA)
- **Solución:** Se implementará en Lab 2 con JWT

---

## 🔄 Próximos Laboratorios

| Lab | Fase | Objetivo |
|-----|------|----------|
| Lab 1 | Despliegue Base | API básica funcionando ✅ |
| Lab 2 | Seguridad | Autenticación JWT + protección |
| Lab 3 | Monitoreo | Health checks y logging |
| Lab 4 | Escalabilidad | Base de datos + caché |

---

## 📝 Notas Adicionales

- El motor de riesgo es **simulado** (para Lab 1). En producción usaría un modelo de ML real.
- La base de datos está **en memoria** (temporal). Lab 3 agregará persistencia.
- Los endpoints están **documentados automáticamente** en Swagger UI.

---

## 🤝 Contribuciones

Este es un proyecto educativo de Roslaysoft Consulting.  
Para preguntas o sugerencias, contacta a tu instructor.

---

**Última actualización:** Junio 2026  
**Roslaysoft Consulting x FinTech Nova**

---

## Ejecución en GitHub Codespaces

### Paso 1. Abrir el proyecto

1. Ingrese al repositorio de GitHub.
2. Seleccione **Code**.
3. Haga clic en **Codespaces**.
4. Cree un nuevo Codespace.

---

### Paso 2. Instalar dependencias

En la terminal ejecute:

```bash
pip install -r requirements.txt
```

---

### Paso 3. Iniciar la API

Ejecute el siguiente comando:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Si todo funciona correctamente, verá un mensaje similar a:

```text
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Endpoints Disponibles

### 1. Página Principal

**GET /**

Devuelve un mensaje de bienvenida.

Ejemplo:

```json
{
  "mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."
}
```

---

### 2. Estado del Sistema

**GET /status**

Permite verificar que la API está funcionando correctamente.

Ejemplo:

```json
{
  "status": "ok",
  "servicios": "operativos"
}
```

---

### 3. Consulta de Datos de Usuario

**GET /datos-sensibles/{usuario}**

Obtiene información asociada a un usuario almacenado en la base de datos simulada.

Ejemplo:

```http
GET /datos-sensibles/user1
```

Respuesta:

```json
{
  "usuario": "user1",
  "estado": "Activo",
  "datos_financieros": "Confidencial"
}
```

---

## Usuarios Disponibles

La base de datos simulada contiene:

| Usuario | Estado |
|----------|----------|
| user1 | Activo |
| user2 | Inactivo |

---

## Documentación Automática

FastAPI genera documentación interactiva automáticamente.

Una vez ejecutada la aplicación, puede acceder a:

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

## Objetivo Académico

Este proyecto fue creado para:

- Comprender el funcionamiento básico de FastAPI.
- Desplegar servicios web en GitHub Codespaces.
- Realizar pruebas de APIs REST.
- Analizar controles de acceso y autenticación.
- Practicar actividades de análisis de vulnerabilidades en entornos controlados.

---

## Tecnologías Utilizadas

- Python
- FastAPI
- Uvicorn

---

## Autor

Proyecto académico para prácticas de desarrollo seguro y análisis de vulnerabilidades.
