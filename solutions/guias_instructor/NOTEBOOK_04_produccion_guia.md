# 🎓 Guía del Instructor - Notebook 04: RAG en Producción
## De Prototipo a Sistema Enterprise con FastAPI

---

## 📋 Información General

**Duración:** 75 minutos (15:30-16:45)
- **Teoría:** 30 min (15:30-16:00)
- **Práctica:** 45 min (16:00-16:45)

**Objetivo:** Llevar RAG a producción con FastAPI, Docker y mejores prácticas
**Nivel:** Avanzado - Enterprise
**Pre-requisitos:** Módulos 1-3 completados

---

## 🎯 Objetivos de Aprendizaje

1. ✅ **Crear** API FastAPI completa para RAG
2. ✅ **Implementar** streaming de respuestas (Server-Sent Events)
3. ✅ **Añadir** autenticación Bearer token
4. ✅ **Configurar** rate limiting por usuario
5. ✅ **Implementar** logging estructurado (Loguru)
6. ✅ **Crear** Docker container
7. ✅ **Deployer** a cloud (Railway/Render)
8. ✅ **Alcanzar** 500ms de latencia con optimizaciones enterprise

---

## 📊 Métricas Target (Sistema en Producción)

| Métrica | Módulo 3 | Módulo 4 (Target) | Mejora |
|---------|----------|-------------------|---------|
| ⏱️ Latencia | 800ms | 500ms | -37% |
| 💰 Costo | $0.006 | $0.004 | -33% |
| 🎯 Accuracy | 85% | 90% | +6% |
| 🔒 Seguridad | Básica | Producción | +++ |
| 📊 Observabilidad | No | Completa | +++ |

---

## 🗓️ Timeline Detallado

| Tiempo | Sección | Actividad | TODOs |
|--------|---------|-----------|-------|
| 15:30-15:45 | Parte 1: FastAPI Base | Endpoints básicos | 1-3 |
| 15:45-16:00 | Parte 2: Features | Streaming, Auth, Rate Limit | 4-6 |
| 16:00-16:15 | Parte 3: Observabilidad | Logging, Monitoring, Health | 7-9 |
| 16:15-16:30 | Parte 4: Containerización | Docker, Docker Compose | 10-11 |
| 16:30-16:45 | Parte 5: Deployment | Deploy y testing | 12 |

---

## 📝 Guión de la Sesión

### PARTE 1: FastAPI Base [15:30-15:45] - 15 min

#### 1. Introducción a Producción (3 min)

**Instructor presenta:**

> "Hasta ahora todo ha sido en notebooks. Ahora vamos a convertirlo en una API de producción lista para recibir millones de requests. FastAPI es el framework más rápido de Python y perfecto para RAG."

**Conceptos clave de producción:**
- **API REST:** Endpoints HTTP para acceso programático
- **Async:** Manejo de múltiples requests simultáneos
- **Streaming:** Respuestas en tiempo real
- **Autenticación:** Solo usuarios autorizados
- **Rate Limiting:** Prevenir abuso
- **Logging:** Trazabilidad de errores
- **Monitoring:** Métricas en tiempo real
- **Docker:** Containerización para deploy
- **CI/CD:** Automatización de deployment

#### 2. Estructura del Proyecto (2 min)

**Mostrar estructura:**
```
src/
├── main.py              # FastAPI app
├── module_4_production.py  # RAG optimizado
├── auth.py              # Autenticación
├── rate_limiter.py      # Rate limiting
└── monitoring.py        # Métricas
```

#### 3. FastAPI Hello World (5 min)

**Ejecutar primer endpoint:**

```python
from fastapi import FastAPI

app = FastAPI(title="RAG Production API")

@app.get("/")
def root():
    return {"message": "RAG API Running", "version": "1.0.0"}
```

**Iniciar servidor:**
```bash
uvicorn main:app --reload
```

**Mostrar en navegador:** http://localhost:8000
**Mostrar docs automáticas:** http://localhost:8000/docs

**💡 Destacar:**
> "FastAPI genera documentación interactiva automáticamente. Esto es oro para APIs."

#### 4. TODO 1: Endpoint de Health Check (5 min)

**Instructor guía implementación:**

```python
@app.get("/health")
async def health_check():
    """Health check para kubernetes/docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": time.time() - start_time,
        "checks": {
            "api": "ok",
            "database": "ok",  # Verificar ChromaDB
            "openai": "ok"     # Verificar API key
        }
    }
```

**Por qué es importante:**
- Kubernetes usa /health para saber si reiniciar container
- Monitoreo puede alertar si algo falla
- Debug rápido de problemas

---

### PARTE 2: Features de Producción [15:45-16:00] - 15 min

#### 5. TODO 2-3: Endpoints de Indexación y Query (7 min)

**Endpoint de indexación:**
```python
@app.post("/index")
async def index_documents(files: List[UploadFile]):
    """Indexar documentos nuevos"""
    # Procesar archivos subidos
    for file in files:
        content = await file.read()
        # Indexar en RAG
    return {"indexed": len(files), "status": "success"}
```

**Endpoint de query:**
```python
@app.post("/query")
async def query_rag(request: QueryRequest):
    """Query al RAG"""
    result = rag_system.query(request.question)
    return {
        "answer": result['response'],
        "sources": result['sources'],
        "metrics": result['metrics']
    }
```

#### 6. TODO 4: Streaming con Server-Sent Events (8 min) ⭐ **FEATURE CRÍTICA**

**Instructor explica:**
> "Streaming permite mostrar la respuesta mientras se genera, como ChatGPT. Mejora UX dramáticamente."

**Implementación:**
```python
from fastapi.responses import StreamingResponse

@app.post("/query/stream")
async def query_stream(request: QueryRequest):
    """Query con streaming"""
    async def generate():
        # Yield chunks a medida que se generan
        for chunk in rag_system.query_stream(request.question):
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

**Demo en vivo:**
- Mostrar query normal (espera 2 segundos, devuelve todo)
- Mostrar query streaming (respuesta aparece inmediatamente, palabra por palabra)

**💡 Impacto UX:**
> "Latencia percibida baja de 2000ms a ~200ms. El usuario ve resultados instantáneamente."

---

### PARTE 3: Seguridad y Observabilidad [16:00-16:15] - 15 min

#### 7. TODO 5-6: Autenticación y Rate Limiting (7 min)

**Autenticación Bearer Token:**
```python
from fastapi import Depends, HTTPException, Header

async def verify_token(authorization: str = Header(...)):
    """Verificar API key del usuario"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid token format")

    token = authorization.split(" ")[1]

    if token not in valid_tokens:
        raise HTTPException(403, "Invalid API key")

    return token

@app.post("/query", dependencies=[Depends(verify_token)])
async def query_rag(request: QueryRequest):
    # Solo accesible con token válido
    ...
```

**Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/query")
@limiter.limit("10/minute")  # Max 10 queries por minuto
async def query_rag(request: QueryRequest):
    ...
```

**Por qué importa:**
- Prevenir abuso de API
- Proteger costos (cada query cuesta $)
- Cumplir con SLAs

#### 8. TODO 7-8: Logging y Monitoring (8 min)

**Logging estructurado con Loguru:**
```python
from loguru import logger

logger.add(
    "logs/rag_api_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

@app.post("/query")
async def query_rag(request: QueryRequest):
    logger.info(f"Query received: {request.question[:50]}...")

    try:
        result = rag_system.query(request.question)
        logger.info(f"Query successful: {result['metrics']['latency']}ms")
        return result
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise
```

**Monitoring con Prometheus:**
```python
from prometheus_client import Counter, Histogram

# Métricas
query_counter = Counter('rag_queries_total', 'Total queries')
query_latency = Histogram('rag_query_latency_seconds', 'Query latency')

@app.post("/query")
async def query_rag(request: QueryRequest):
    query_counter.inc()

    with query_latency.time():
        result = rag_system.query(request.question)

    return result
```

**Dashboard de métricas:**
- Queries por segundo
- Latencia p50, p95, p99
- Error rate
- Costo acumulado

---

### PARTE 4: Containerización [16:15-16:30] - 15 min

#### 9. TODO 10: Dockerfile (7 min)

**Instructor crea Dockerfile en vivo:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src/ ./src/
COPY data/ ./data/

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build y run:**
```bash
# Build
docker build -t rag-api:latest .

# Run
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  rag-api:latest
```

**Test:**
```bash
curl http://localhost:8000/health
```

#### 10. TODO 11: Docker Compose (8 min)

**Para apps con múltiples servicios:**

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

volumes:
  redis_data:
```

**Iniciar todo:**
```bash
docker-compose up -d
```

---

### PARTE 5: Deployment [16:30-16:45] - 15 min

#### 11. TODO 12: Deploy a Cloud (10 min)

**Opciones de deployment:**

**Opción A: Railway (Más simple)**
```bash
# 1. Install CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy
railway init
railway up
```

**Opción B: Render (Free tier)**
- Conectar repo GitHub
- Auto-deploy en cada push
- HTTPS gratis

**Opción C: Google Cloud Run (Escalable)**
```bash
gcloud run deploy rag-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

**Demo de deployment:**
1. Mostrar Railway dashboard
2. Hacer deploy
3. Obtener URL pública
4. Testear desde Postman

#### 12. Testing de API en Producción (5 min)

**Test script:**
```python
import requests

API_URL = "https://rag-api-xxx.railway.app"
API_KEY = "Bearer your-key-here"

# Test health
response = requests.get(f"{API_URL}/health")
print(f"Health: {response.json()}")

# Test query
response = requests.post(
    f"{API_URL}/query",
    headers={"Authorization": API_KEY},
    json={"question": "¿Cuál es la política de vacaciones?"}
)
print(f"Answer: {response.json()['answer']}")
```

**Load testing (opcional):**
```bash
# Usando hey
hey -n 1000 -c 10 -m POST \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"question":"test"}' \
  $API_URL/query
```

---

## 🎉 Resumen del Módulo

### ✅ Lo que construyeron:

1. **API FastAPI** con endpoints de producción
2. **Streaming** de respuestas en tiempo real
3. **Autenticación** Bearer token
4. **Rate limiting** para prevenir abuso
5. **Logging** estructurado con Loguru
6. **Monitoring** con Prometheus
7. **Docker** containerizado
8. **Deployed** a cloud (Railway/Render)

### 📊 Métricas Finales:

| Métrica | Inicio (M1) | Final (M4) | Mejora Total |
|---------|-------------|------------|--------------|
| Latencia | 2000ms | 500ms | **-75%** |
| Costo | $0.010 | $0.004 | **-60%** |
| Accuracy | 70% | 90% | **+29%** |
| Prod-Ready | No | Sí | **✅** |

### 🚀 Sistema Listo para Producción:

✅ API REST escalable
✅ Streaming para UX mejorado
✅ Seguridad enterprise
✅ Observabilidad completa
✅ Containerizado
✅ Deployed a cloud

---

## 📊 Métricas de Éxito del Módulo

- [ ] **90%+** tienen API FastAPI corriendo localmente
- [ ] **80%+** implementaron streaming exitosamente
- [ ] **75%+** añadieron autenticación y rate limiting
- [ ] **70%+** crearon Docker container
- [ ] **50%+** hicieron deployment a cloud

---

## 🚨 Troubleshooting

### Docker build falla
```bash
# Ver logs detallados
docker build --progress=plain -t rag-api .

# Limpiar cache
docker system prune -a
```

### Railway deployment falla
- Verificar Procfile existe
- Verificar requirements.txt completo
- Checar variables de entorno

### Streaming no funciona
- Usar `yield` no `return`
- Content-Type: `text/event-stream`
- Flush cada chunk

---

## ✅ Checklist del Instructor

**Antes:**
- [ ] Probar API localmente
- [ ] Test Docker build
- [ ] Verificar cuenta Railway/Render
- [ ] Preparar API keys de demo

**Durante:**
- [ ] Demo streaming en vivo
- [ ] Mostrar logs en tiempo real
- [ ] Test de carga opcional
- [ ] Deploy a cloud en vivo

**Después:**
- [ ] Verificar deployments exitosos
- [ ] Compartir URLs de APIs deployed
- [ ] Recopilar feedback

---

**🎉 ¡Tienen un RAG de producción enterprise-grade!**
