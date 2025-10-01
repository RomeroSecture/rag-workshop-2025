# Soluciones Notebook 04: Producción - NIVEL 2 WORKSHOP

## 📋 TODOs del Módulo 4

El notebook 04 contiene un archivo completo `module_4_api.py` con 12 TODOs para que los participantes completen. Los TODOs están divididos en:

- **REQUERIDOS** (3 TODOs): Fundamentales para funcionamiento básico
- **RECOMENDADOS** (7 TODOs): Importantes para producción
- **OPCIONALES** (2 TODOs): Mejoras avanzadas

## ✅ Estado Actual (Post-Corrección)

### Mejoras Realizadas:
1. ✅ Redis con fallback automático (funciona sin Redis)
2. ✅ Rate limiting implementado como ejemplo
3. ✅ L1 cache completamente funcional
4. ✅ Métricas collector funcional
5. ✅ Hints comprehensivos en cada TODO
6. ✅ Dockerfile con curl para healthcheck

## 🎯 Soluciones por TODO

### TODO 1: Añadir validación adicional (OPCIONAL)

**Ubicación**: QueryRequest model, línea ~52

**Solución Básica**:
```python
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    user_id: Optional[str] = Field(None, description="ID del usuario")
    use_cache: bool = Field(True, description="Usar cache")

    # TODO 1 - Solución
    language: Optional[str] = Field("es", description="Idioma (es/en)")
    detail_level: Optional[str] = Field("basic", description="Nivel de detalle (basic/complete)")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")
```

**Solución Avanzada con Validators**:
```python
from pydantic import validator

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    user_id: Optional[str] = Field(None, description="ID del usuario")
    use_cache: bool = Field(True, description="Usar cache")
    language: Optional[str] = Field("es", description="Idioma")
    detail_level: Optional[str] = Field("basic", description="Nivel de detalle")

    @validator('question')
    def validate_question(cls, v):
        """Validar que la pregunta no contenga contenido inapropiado"""
        forbidden_words = ['hack', 'exploit', 'bypass']
        if any(word in v.lower() for word in forbidden_words):
            raise ValueError('Pregunta contiene contenido inapropiado')
        return v.strip()

    @validator('language')
    def validate_language(cls, v):
        """Solo permitir idiomas soportados"""
        allowed = ['es', 'en', 'fr', 'de']
        if v not in allowed:
            raise ValueError(f'Idioma debe ser uno de: {allowed}')
        return v

    @validator('detail_level')
    def validate_detail_level(cls, v):
        """Validar nivel de detalle"""
        allowed = ['basic', 'complete', 'technical']
        if v not in allowed:
            raise ValueError(f'Detail level debe ser uno de: {allowed}')
        return v
```

---

### TODO 2: Añadir campos adicionales al response (OPCIONAL)

**Ubicación**: QueryResponse model, línea ~66

**Solución**:
```python
class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    latency_ms: float
    cache_hit: bool
    timestamp: datetime

    # TODO 2 - Solución
    confidence_score: Optional[float] = Field(None, description="Confianza 0-1")
    model_used: Optional[str] = Field("gpt-3.5-turbo", description="Modelo LLM usado")
    tokens_used: Optional[int] = Field(None, description="Tokens consumidos")
    query_id: Optional[str] = Field(None, description="UUID único del query")
    warning: Optional[str] = Field(None, description="Advertencias si hay")
```

**Uso en el endpoint**:
```python
import uuid

# Dentro del endpoint /query
return QueryResponse(
    answer=answer,
    sources=sources,
    latency_ms=latency,
    cache_hit=cache_hit,
    timestamp=datetime.now(),
    # Campos adicionales
    confidence_score=result.get("confidence", 0.85),
    model_used="gpt-3.5-turbo",
    tokens_used=result.get("tokens_used", 150),
    query_id=str(uuid.uuid4()),
    warning=None if len(sources) > 0 else "Pocas fuentes encontradas"
)
```

---

### TODO 3: Implementar búsqueda en L1 (REQUERIDO)

**Ubicación**: MultiLevelCache.get(), línea ~106

**Estado**: ✅ **YA IMPLEMENTADO** como ejemplo

```python
def get(self, key: str) -> Optional[Dict]:
    # L1: Búsqueda exacta en memoria (5ms)
    if key in self.l1_cache:
        self.l1_access_count[key] = self.l1_access_count.get(key, 0) + 1
        logger.info(f"✅ Cache L1 HIT: {key[:10]}")
        return self.l1_cache[key]
```

**Explicación**: Este TODO ya está completo como ejemplo para que los participantes vean cómo funciona el patrón antes de implementar L2 y L3.

---

### TODO 4: Implementar búsqueda en Redis (RECOMENDADO)

**Ubicación**: MultiLevelCache.get(), línea ~117

**Estado**: ✅ **YA IMPLEMENTADO** con fallback automático

```python
# L2: Redis (10ms) - Solo si está disponible
if self.redis_available:
    try:
        cached_value = self.redis_client.get(key)
        if cached_value:
            result = json.loads(cached_value)
            # Promocionar a L1
            self.set_l1(key, result)
            logger.info(f"✅ Cache L2 HIT: {key[:10]}")
            return result
    except Exception as e:
        logger.warning(f"Redis error: {e}")
```

**Explicación**: Implementado con try-except para que funcione sin Redis instalado.

---

### TODO 5: Implementar búsqueda semántica (OPCIONAL - AVANZADO)

**Ubicación**: MultiLevelCache.get(), línea ~134

**Solución Completa**:
```python
# L3: Semantic similarity (50ms)
def get(self, key: str) -> Optional[Dict]:
    # ... código L1 y L2 ...

    # L3: Semantic similarity
    if hasattr(self, 'embedder'):
        try:
            # Generar embedding de la query
            query_embedding = self.embedder.embed(key)

            # Buscar en cache semántico
            best_match = None
            best_similarity = 0.95  # Threshold alto

            for cached_key, cached_data in self.semantic_cache.items():
                cached_embedding = cached_data.get('embedding')
                if cached_embedding:
                    # Calcular similaridad coseno
                    similarity = self._cosine_similarity(
                        query_embedding,
                        cached_embedding
                    )

                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = cached_data.get('result')

            if best_match:
                logger.info(f"✅ Cache L3 HIT (similarity: {best_similarity:.2f})")
                # Promocionar a L1 y L2
                self.set(key, best_match)
                return best_match

        except Exception as e:
            logger.warning(f"Semantic cache error: {e}")

    logger.info(f"❌ Cache MISS: {key[:10]}")
    return None

def _cosine_similarity(self, vec1, vec2):
    """Calcular similaridad coseno entre dos vectores"""
    import numpy as np
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)
```

**Nota**: Este es avanzado y requiere embedder configurado. Opcional para workshop.

---

### TODO 6: Implementar guardado en L1 (REQUERIDO)

**Ubicación**: MultiLevelCache.set(), línea ~146

**Estado**: ✅ **YA IMPLEMENTADO**

```python
def set(self, key: str, value: Dict):
    # Guardar en L1
    self.set_l1(key, value)
```

**Explicación**: Delega a `set_l1()` que implementa política LRU.

---

### TODO 7: Implementar guardado en Redis (RECOMENDADO)

**Ubicación**: MultiLevelCache.set(), línea ~149

**Estado**: ✅ **YA IMPLEMENTADO**

```python
# Guardar en Redis con TTL
if self.redis_available:
    try:
        self.redis_client.set(
            key,
            json.dumps(value, default=str),
            ex=3600  # TTL 1 hora
        )
    except Exception as e:
        logger.warning(f"Redis set error: {e}")
```

---

### TODO 8: Implementar rate limiting (RECOMENDADO)

**Ubicación**: RateLimiter.check_rate_limit(), línea ~176

**Estado**: ✅ **YA IMPLEMENTADO** con sliding window

```python
def check_rate_limit(self, user_id: str) -> bool:
    """Verificar si usuario excede límite (sliding window)"""
    current_time = time.time()

    # Inicializar si es nuevo usuario
    if user_id not in self.requests:
        self.requests[user_id] = []

    # Filtrar requests del último minuto
    minute_ago = current_time - 60
    self.requests[user_id] = [
        ts for ts in self.requests[user_id]
        if ts > minute_ago
    ]

    # Verificar límite
    if len(self.requests[user_id]) >= self.requests_per_minute:
        logger.warning(f"❌ Rate limit exceeded for {user_id}")
        return False

    # Añadir request actual
    self.requests[user_id].append(current_time)
    return True
```

**Algoritmo**: Sliding window - mantiene timestamps de requests y filtra los del último minuto.

---

### TODO 9: Implementar registro de métricas (REQUERIDO)

**Ubicación**: MetricsCollector.record_request(), línea ~204

**Estado**: ✅ **YA IMPLEMENTADO**

```python
def record_request(self, latency: float, cache_hit: bool):
    """Registrar métricas de request"""
    self.metrics["total_requests"] += 1
    self.metrics["total_latency"] += latency

    if cache_hit:
        self.metrics["cache_hits"] += 1
    else:
        self.metrics["cache_misses"] += 1

    # Calcular promedio
    if self.metrics["total_requests"] > 0:
        self.metrics["avg_latency"] = (
            self.metrics["total_latency"] / self.metrics["total_requests"]
        )
```

---

### TODO 10: Inicializar sistema RAG (REQUERIDO)

**Ubicación**: get_rag_system(), línea ~231

**Solución - Opción A (LangChain)**:
```python
@lru_cache()
def get_rag_system():
    """Singleton del sistema RAG"""
    logger.info("🔧 Inicializando sistema RAG...")

    from module_3_advanced import Module3_AdvancedRAG

    rag = Module3_AdvancedRAG()

    # Cargar e indexar documento
    doc = rag.load_document("../data/company_handbook.pdf")
    chunks = rag.create_chunks(doc)
    rag.index_chunks(chunks)

    logger.info("✅ RAG system initialized")
    return rag
```

**Solución - Opción B (Módulo 2)**:
```python
@lru_cache()
def get_rag_system():
    """Singleton del sistema RAG"""
    from module_2_optimized import Module2_OptimizedRAG

    rag = Module2_OptimizedRAG()

    # Setup inicial
    doc = rag.load_document("../data/company_handbook.pdf")
    chunks = rag.create_chunks(doc, chunk_size=1000, chunk_overlap=200)
    rag.index_chunks(chunks)

    return rag
```

**Solución - Opción C (LlamaIndex)**:
```python
@lru_cache()
def get_rag_system():
    """Singleton del sistema RAG con LlamaIndex"""
    from llama_index import VectorStoreIndex, SimpleDirectoryReader
    from llama_index.llms import OpenAI

    # Cargar documentos
    documents = SimpleDirectoryReader('../data').load_data()

    # Crear índice
    index = VectorStoreIndex.from_documents(documents)

    # Query engine
    query_engine = index.as_query_engine(
        llm=OpenAI(temperature=0.3),
        similarity_top_k=3
    )

    # Wrapper para compatibilidad
    class RAGWrapper:
        def __init__(self, engine):
            self.engine = engine

        def query(self, question):
            response = self.engine.query(question)
            return {
                "answer": str(response),
                "sources": [{"text": node.text, "score": node.score}
                           for node in response.source_nodes],
                "latency_ms": 0  # LlamaIndex no trackea esto por defecto
            }

    return RAGWrapper(query_engine)
```

---

### TODO 11: Añadir autenticación (RECOMENDADO)

**Ubicación**: /cache endpoint, línea ~333

**Solución**:
```python
from fastapi.security import APIKeyHeader
from fastapi import Security

# Configurar API Key
API_KEY = "your-secret-api-key-here"  # En producción: usar env var
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verificar API key"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API Key"
        )
    return api_key

@app.delete("/cache")
async def clear_cache(api_key: str = Depends(verify_api_key)):
    """Limpiar cache (requiere autenticación)"""

    cache.l1_cache.clear()
    cache.l1_access_count.clear()

    if cache.redis_available:
        try:
            cache.redis_client.flushdb()
        except:
            pass

    logger.info("🗑️  Cache limpiado")
    return {"status": "cache cleared", "timestamp": datetime.now()}
```

**Uso**:
```bash
# Con autenticación
curl -X DELETE http://localhost:8000/cache \
  -H "X-API-Key: your-secret-api-key-here"
```

---

### TODO 12: Guardar métricas finales (OPCIONAL)

**Ubicación**: shutdown_event(), línea ~350

**Solución**:
```python
import json
from pathlib import Path

@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al apagar"""
    logger.info("👋 Shutting down RAG API...")

    # TODO 12 - Solución
    final_metrics = metrics.get_metrics()

    # Guardar en archivo
    metrics_dir = Path("logs/metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)

    metrics_file = metrics_dir / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(metrics_file, 'w') as f:
        json.dump({
            "shutdown_time": datetime.now().isoformat(),
            "metrics": final_metrics,
            "uptime_seconds": time.time() - startup_time  # Requiere global startup_time
        }, f, indent=2)

    logger.info(f"📊 Métricas guardadas en: {metrics_file}")

    # Opcional: Enviar a sistema de monitoring
    try:
        # Ejemplo con webhook
        import requests
        requests.post(
            "https://your-monitoring-service.com/metrics",
            json=final_metrics,
            timeout=5
        )
    except:
        pass
```

**Para trackear uptime, añade al startup**:
```python
startup_time = None

@app.on_event("startup")
async def startup_event():
    global startup_time
    startup_time = time.time()
    logger.info("🚀 Starting RAG API...")
    get_rag_system()
    logger.info("✅ RAG API ready!")
```

---

## 📊 Resumen de TODOs

| TODO | Estado | Dificultad | Prioridad |
|------|--------|------------|-----------|
| 1. Validación adicional | Opcional | Baja | Baja |
| 2. Campos response | Opcional | Baja | Media |
| 3. Búsqueda L1 | ✅ Implementado | Baja | Alta |
| 4. Búsqueda Redis | ✅ Implementado | Media | Alta |
| 5. Búsqueda semántica | Pendiente | Alta | Baja |
| 6. Guardado L1 | ✅ Implementado | Baja | Alta |
| 7. Guardado Redis | ✅ Implementado | Media | Alta |
| 8. Rate limiting | ✅ Implementado | Media | Alta |
| 9. Métricas | ✅ Implementado | Baja | Alta |
| 10. Init RAG | Pendiente | Media | **CRÍTICA** |
| 11. Autenticación | Pendiente | Media | Alta |
| 12. Guardar métricas | Opcional | Baja | Baja |

**Para completar el workshop mínimo**:
- TODO 10 (Inicializar RAG) - **OBLIGATORIO**
- TODOs 3, 4, 6, 7, 8, 9 - **Ya implementados como ejemplos**

**Para producción real**:
- TODO 11 (Autenticación) - **Muy recomendado**
- TODO 1, 2 (Validaciones) - Recomendado
- TODO 5 (Semantic cache) - Avanzado, opcional
- TODO 12 (Guardar métricas) - Nice to have

---

## 🚀 Testing Completo

Una vez completados los TODOs, verificar:

```bash
# 1. Iniciar API
python src/module_4_api.py

# 2. Test health
curl http://localhost:8000/

# 3. Test query sin cache
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Política de vacaciones?", "use_cache": false}'

# 4. Test query con cache (mismo query)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Política de vacaciones?", "use_cache": true}'

# 5. Ver métricas
curl http://localhost:8000/metrics

# 6. Limpiar cache (si implementaste autenticación)
curl -X DELETE http://localhost:8000/cache \
  -H "X-API-Key: your-key-here"
```

**Resultados esperados**:
- Primera query: ~500-1000ms (sin cache)
- Segunda query: ~5ms (L1 cache hit)
- Cache hit rate: >50% después de varias queries

---

## ✅ Checklist de Completitud

- [ ] API arranca sin errores
- [ ] Endpoint /query funciona
- [ ] L1 cache funcional (5ms)
- [ ] Redis funciona (o fallback activo)
- [ ] Rate limiting protege contra abuso
- [ ] Métricas se registran correctamente
- [ ] Logs son informativos
- [ ] Docker build exitoso
- [ ] Docker-compose levanta todos los servicios

**🎉 Módulo 4 completo cuando todos los checks pasan!**
