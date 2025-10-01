# 🔒 Soluciones del Workshop RAG 2025

**⚠️ SOLO PARA INSTRUCTORES - NO COMPARTIR CON PARTICIPANTES**

## 📁 Estructura de Soluciones

Este directorio contiene soluciones completas para todos los ejercicios del workshop, organizadas en 3 niveles de complejidad:

### 📊 Niveles de Solución

#### 🟢 Nivel 1: BÁSICO
**Objetivo**: Código mínimo para hacer funcionar el ejercicio

- ✅ Cumple con el requisito funcional
- ⚠️ Sin optimizaciones
- ⚠️ Sin manejo de errores avanzado
- ⚠️ Sin logs detallados
- 🎯 **Uso**: Desbloquear participantes atascados en lo fundamental

**Ejemplo**:
```python
# Solo lo mínimo para que funcione
def query(self, question):
    embedding = self.embedder.embed(question)
    results = self.vectordb.search(embedding, k=3)
    context = "\n".join([r['text'] for r in results])
    return self.llm.generate(question, context)
```

#### 🟡 Nivel 2: WORKSHOP
**Objetivo**: Solución esperada durante el workshop

- ✅ Funcionalidad completa
- ✅ Manejo básico de errores
- ✅ Logs informativos
- ✅ Comentarios explicativos
- ⚡ Optimizaciones básicas
- 🎯 **Uso**: Referencia de lo que se espera que logren

**Ejemplo**:
```python
def query(self, question: str, k: int = 3) -> Dict[str, Any]:
    """Query con manejo de errores y logging básico"""
    try:
        logger.info(f"Query recibida: {question}")

        # Generar embedding
        embedding = self.embedder.embed(question)

        # Búsqueda en vectordb
        results = self.vectordb.search(embedding, k=k)

        if not results:
            logger.warning("No se encontraron resultados")
            return {"answer": "No encontré información relevante", "sources": []}

        # Construir contexto
        context = "\n\n".join([
            f"[Fuente {i+1}]: {r['text']}"
            for i, r in enumerate(results)
        ])

        # Generar respuesta
        answer = self.llm.generate(question, context)

        logger.info(f"Respuesta generada exitosamente")
        return {
            "answer": answer,
            "sources": [r['metadata'] for r in results],
            "num_sources": len(results)
        }

    except Exception as e:
        logger.error(f"Error en query: {e}")
        raise
```

#### 🔴 Nivel 3: PRODUCCIÓN
**Objetivo**: Código production-ready con mejores prácticas

- ✅ Funcionalidad completa y robusta
- ✅ Manejo exhaustivo de errores
- ✅ Logging estructurado con contexto
- ✅ Type hints completos
- ✅ Validación de inputs
- ✅ Métricas y observabilidad
- ✅ Tests unitarios
- ✅ Documentación completa
- ⚡ Optimizaciones avanzadas
- 🔒 Seguridad (rate limiting, sanitización)
- 🎯 **Uso**: Mostrar best practices y camino de evolución

**Ejemplo**:
```python
@lru_cache(maxsize=1000)
async def query(
    self,
    question: str,
    k: int = 3,
    temperature: float = 0.7,
    timeout: float = 30.0,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> QueryResult:
    """
    Query production-ready con caching, async, métricas y seguridad.

    Args:
        question: Pregunta del usuario (max 500 chars)
        k: Número de documentos a recuperar (1-10)
        temperature: Temperatura del LLM (0.0-1.0)
        timeout: Timeout en segundos
        metadata_filter: Filtros opcionales para búsqueda

    Returns:
        QueryResult con answer, sources, metrics y metadata

    Raises:
        ValueError: Si los parámetros son inválidos
        TimeoutError: Si excede el timeout
        RAGException: Para otros errores del sistema
    """
    # Validación de inputs
    if not question or len(question.strip()) == 0:
        raise ValueError("La pregunta no puede estar vacía")

    if len(question) > 500:
        raise ValueError("La pregunta excede el límite de 500 caracteres")

    if not 1 <= k <= 10:
        raise ValueError("k debe estar entre 1 y 10")

    if not 0.0 <= temperature <= 1.0:
        raise ValueError("temperature debe estar entre 0.0 y 1.0")

    # Sanitización
    question = self._sanitize_input(question)

    # Inicio de métricas
    start_time = time.time()
    query_id = str(uuid.uuid4())

    logger.info(
        "query_started",
        extra={
            "query_id": query_id,
            "question_length": len(question),
            "k": k,
            "temperature": temperature
        }
    )

    try:
        # Rate limiting
        await self.rate_limiter.acquire(question)

        # Generar embedding con timeout
        async with asyncio.timeout(timeout * 0.3):
            embedding = await self.embedder.embed_async(question)

        # Búsqueda vectorial con métricas
        search_start = time.time()
        results = await self.vectordb.search_async(
            embedding=embedding,
            k=k,
            filters=metadata_filter,
            timeout=timeout * 0.3
        )
        search_latency = time.time() - search_start

        if not results:
            logger.warning(
                "no_results_found",
                extra={"query_id": query_id}
            )
            return QueryResult(
                answer="No encontré información relevante para tu pregunta.",
                sources=[],
                query_id=query_id,
                latency_ms=int((time.time() - start_time) * 1000),
                cache_hit=False
            )

        # Construcción de contexto con reranking opcional
        context = await self._build_context(results, question)

        # Generación LLM con streaming
        llm_start = time.time()
        async with asyncio.timeout(timeout * 0.4):
            answer = await self.llm.generate_async(
                question=question,
                context=context,
                temperature=temperature
            )
        llm_latency = time.time() - llm_start

        # Métricas finales
        total_latency = time.time() - start_time

        # Logging estructurado
        logger.info(
            "query_completed",
            extra={
                "query_id": query_id,
                "total_latency_ms": int(total_latency * 1000),
                "search_latency_ms": int(search_latency * 1000),
                "llm_latency_ms": int(llm_latency * 1000),
                "num_sources": len(results),
                "answer_length": len(answer)
            }
        )

        # Incrementar métricas de Prometheus
        self.metrics.query_counter.inc()
        self.metrics.query_latency.observe(total_latency)

        return QueryResult(
            answer=answer,
            sources=[r.metadata for r in results],
            query_id=query_id,
            latency_ms=int(total_latency * 1000),
            cache_hit=False,
            metrics={
                "search_latency_ms": int(search_latency * 1000),
                "llm_latency_ms": int(llm_latency * 1000),
                "num_sources": len(results)
            }
        )

    except asyncio.TimeoutError:
        logger.error(
            "query_timeout",
            extra={"query_id": query_id, "timeout": timeout}
        )
        raise TimeoutError(f"Query excedió el timeout de {timeout}s")

    except Exception as e:
        logger.error(
            "query_failed",
            extra={
                "query_id": query_id,
                "error_type": type(e).__name__,
                "error_message": str(e)
            },
            exc_info=True
        )
        self.metrics.query_errors.inc()
        raise RAGException(f"Error en query: {str(e)}") from e
```

---

## 📚 Notebooks con Soluciones

### Notebook 02: Arquitectura y Optimización
- **TODOs**: 5 ejercicios
- **Archivos**:
  - `nivel_1_basico/02_arquitectura_solucion.ipynb`
  - `nivel_2_workshop/02_arquitectura_solucion.ipynb`
  - `nivel_3_produccion/02_arquitectura_solucion.ipynb`

### Notebook 03: Frameworks (LangChain, LlamaIndex)
- **TODOs**: 8 ejercicios (3 paths)
- **Archivos**:
  - `nivel_1_basico/03_frameworks_solucion.ipynb`
  - `nivel_2_workshop/03_frameworks_solucion.ipynb`
  - `nivel_3_produccion/03_frameworks_solucion.ipynb`

### Notebook 04: Producción y Escalado
- **TODOs**: 12 ejercicios
- **Archivos**:
  - `nivel_1_basico/04_produccion_solucion.ipynb`
  - `nivel_2_workshop/04_produccion_solucion.ipynb`
  - `nivel_3_produccion/04_produccion_solucion.ipynb`

### Notebook 05: Proyecto Final
- **TODOs**: Proyecto abierto
- **Archivos**:
  - `nivel_1_basico/05_proyecto_ejemplos/` (3 casos de uso básicos)
  - `nivel_2_workshop/05_proyecto_ejemplos/` (3 casos completos)
  - `nivel_3_produccion/05_proyecto_ejemplos/` (3 casos production-ready)

---

## 🎯 Guía de Uso Durante el Workshop

### Situación 1: Participante Bloqueado
1. Identificar el ejercicio específico (ej: "Notebook 02, TODO #3")
2. Abrir **Nivel 1 BÁSICO** correspondiente
3. Mostrar SOLO el código del ejercicio específico (no todo el notebook)
4. Explicar la lógica sin dar la solución completa
5. Dejar que complete los detalles

### Situación 2: Participante Adelantado
1. Si termina rápido, mostrar **Nivel 3 PRODUCCIÓN**
2. Desafiar a mejorar su código hacia ese nivel
3. Discutir diferencias y trade-offs

### Situación 3: Demostración Post-Workshop
1. Usar **Nivel 2 WORKSHOP** como referencia
2. Comparar con código de participantes
3. Destacar puntos clave y mejoras

### Situación 4: Dudas Conceptuales
1. Usar **Nivel 3 PRODUCCIÓN** para explicar conceptos avanzados
2. Mostrar evolución desde básico → producción
3. Discutir mejores prácticas

---

## 🔐 Acceso y Seguridad

- ⚠️ **NUNCA** compartir esta rama con participantes
- ⚠️ **NUNCA** pushear a `main` accidentalmente
- ✅ Mantener en rama `solutions` separada
- ✅ Solo instructores tienen acceso
- ✅ Revisar antes de compartir pantalla

---

## 📝 Checklist de Uso

Antes del workshop:
- [ ] Revisar todas las soluciones
- [ ] Probar que funcionen correctamente
- [ ] Familiarizarse con diferencias entre niveles
- [ ] Preparar snippets de código frecuentes

Durante el workshop:
- [ ] Tener esta rama abierta en ventana separada
- [ ] Usar Nivel 1 para desbloqueos rápidos
- [ ] Usar Nivel 2 como referencia esperada
- [ ] Usar Nivel 3 para participantes avanzados

Después del workshop:
- [ ] Actualizar soluciones basándose en feedback
- [ ] Documentar preguntas frecuentes
- [ ] Mejorar hints en main branch si es necesario

---

**Contacto**: aromero@secture.com

*Creado para maximizar el aprendizaje de los participantes* 🎓
