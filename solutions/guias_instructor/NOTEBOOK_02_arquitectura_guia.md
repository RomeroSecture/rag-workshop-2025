# 🎓 Guía del Instructor - Notebook 02: Arquitectura y Optimización
## Reduciendo Latencia 50% y Mejorando Calidad

---

## 📋 Información General

**Duración:** 90 minutos (10:45-12:15 con break 12:15-12:30)
- **Teoría:** 45 min (10:45-11:30)
- **Práctica:** 45 min (11:30-12:15)
- **Break:** 15 min (12:15-12:30)

**Objetivo:** Optimizar el RAG básico para mejorar latencia, costo y calidad
**Nivel:** Intermedio
**Pre-requisitos:** Haber completado Módulo 1 (SimpleRAG funcional)

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este módulo, los participantes serán capaces de:

1. ✅ **Implementar** chunking con overlap para preservar contexto
2. ✅ **Aplicar** caching para queries repetidas (speedup 10x)
3. ✅ **Crear** prompts optimizados y especializados
4. ✅ **Implementar** re-ranking de resultados semánticos
5. ✅ **Optimizar** parámetros del LLM (temperature, max_tokens)
6. ✅ **Reducir** latencia de 2000ms → 1000ms (-50%)
7. ✅ **Mejorar** accuracy de 70% → 80% (+10%)

---

## 📊 Métricas Target

| Métrica | Módulo 1 (Baseline) | Módulo 2 (Target) | Mejora |
|---------|---------------------|-------------------|---------|
| ⏱️ Latencia | 2000ms | 1000ms | -50% |
| 💰 Costo | $0.010 | $0.008 | -20% |
| 🎯 Accuracy | 70% | 80% | +10% |

---

## 🗓️ Timeline Detallado

| Tiempo | Sección | Actividad | Celdas |
|--------|---------|-----------|--------|
| 10:45-11:00 | Parte 1: Comparación | Baseline vs Optimized | 1-5 |
| 11:00-11:30 | Parte 2: Optimizaciones | Cache, Rerank, Metadatos | 6-9 |
| 11:30-11:45 | Parte 3: Prompts | Templates y Temperature | 10-12 |
| 11:45-12:05 | Parte 4: Benchmark | Comparación final | 13-15 |
| 12:05-12:15 | Ejercicios | Práctica guiada | 16-19 |

---

## 📝 Guión de la Sesión

### PARTE 1: Comparación con Módulo 1 [10:45-11:00] - 15 min

#### 1. Setup y Contexto (3 min)

**Instructor presenta:**

> "En Módulo 1 construimos un RAG funcional pero básico. Ahora vamos a optimizarlo profesionalmente. Al final de este módulo tendrán un sistema 2x más rápido y 15% más preciso."

**Ejecutar Celda 2:**
```python
from module_1_basics import Module1_BasicRAG
from module_2_optimized import Module2_OptimizedRAG

rag_v1 = Module1_BasicRAG()  # Baseline
rag_v2 = Module2_OptimizedRAG()  # Optimizado
```

**Mostrar configuraciones:**
```
📊 Configuración:
Módulo 1: chunk_size=500, overlap=0
Módulo 2: chunk_size=1000, overlap=200
```

**Explicar cambios clave:**
- **Chunk size mayor:** 500 → 1000 chars (más contexto por chunk)
- **Overlap:** 0 → 200 chars (preserva contexto entre chunks)
- **Cache:** No → Sí (respuestas instantáneas para queries repetidas)
- **Re-ranking:** No → Sí (mejora relevancia)

#### 2. Chunking Mejorado (7 min)

**Instructor ejecuta Celda 4:**

```python
# Cargar mismo documento
doc = rag_v1.load_document()

# Chunking v1 (sin overlap)
chunks_v1 = rag_v1.create_chunks(doc)  # → 91 chunks

# Chunking v2 (con overlap)
chunks_v2 = rag_v2.create_chunks(doc)  # → 114 chunks
```

**Resultados típicos:**
```
📊 Resultados:
V1 (sin overlap): 91 chunks
V2 (con overlap): 114 chunks (+23 chunks, +25%)
```

**Explicar por qué más chunks:**
- Cada chunk de 1000 chars
- Se avanza solo 800 chars (1000-200 overlap)
- Los últimos 200 chars de cada chunk se repiten en el siguiente
- Esto preserva contexto entre boundaries

**Análisis de cobertura:**
```python
test_phrase = "política de vacaciones"
v1_contains = sum(1 for c in chunks_v1 if test_phrase in c.lower())  # → 1
v2_contains = sum(1 for c in chunks_v2 if test_phrase in c.lower())  # → 2
```

**💡 Insight clave:**
> "Con overlap, frases que caían en boundaries ahora aparecen completas en 2 chunks. Esto mejora mucho la búsqueda semántica."

**Ejecutar Celda 5 (visualización):**

**Diagrama sin overlap:**
```
[Chunk 1: 0-1000][Chunk 2: 1000-2000][Chunk 3: 2000-3000]
                  ↑ Aquí se pierde contexto
```

**Diagrama con overlap:**
```
[Chunk 1: 0-1000]
     [Chunk 2: 800-1800]
          [Chunk 3: 1600-2600]
  🔴 = Zonas de overlap (contexto compartido)
```

**Analogía útil:**
> "Es como leer un libro con binoculares: siempre mantienes un poco del contenido anterior visible mientras avanzas."

---

### PARTE 2: Optimizaciones Avanzadas [11:00-11:30] - 30 min

#### 3. Indexación Optimizada (5 min)

**Instructor ejecuta Celda 7:**

```python
# Módulo 1
start = time.time()
rag_v1.index_chunks(chunks_v1[:20])
v1_time = (time.time() - start) * 1000  # ~1,200ms

# Módulo 2 (con metadatos)
start = time.time()
rag_v2.index_chunks(chunks_v2[:25])
v2_time = (time.time() - start) * 1000  # ~1,400ms
```

**Explicar por qué es ligeramente más lento:**
- V2 procesa más chunks (25 vs 20)
- V2 añade metadatos a cada chunk:
  - `chunk_id`: Identificador único
  - `position`: Posición en documento
  - `source`: Nombre del documento
  - `timestamp`: Cuándo se indexó

**Valor de los metadatos:**
```python
# Permitirá filtrar resultados
results = rag_v2.search_with_metadata(
    query="vacaciones",
    filters={"source": "company_handbook.pdf"}
)
```

#### 4. Caching Inteligente (8 min) ⭐ CORE FEATURE

**Instructor ejecuta Celda 8:**

```python
query_test = "¿Cuál es la política de vacaciones?"

# Primera ejecución (sin cache)
result1 = rag_v2.query(query_test)
time1 = result1['metrics']['total_time_ms']  # ~1,800ms

# Segunda ejecución (CON cache)
result2 = rag_v2.query(query_test)
time2 = result2['metrics']['total_time_ms']  # ~150ms
```

**Resultados esperados:**
```
📊 Mejora por cache:
Sin cache: 1,823ms
Con cache: 147ms
Speedup: 12.4x más rápido
Ahorro: 1,676ms
```

**Explicar cómo funciona el cache:**

```python
# Pseudo-código del cache
def query(self, question):
    cache_key = hashlib.md5(question.encode()).hexdigest()

    # Revisar cache
    if cache_key in self.cache:
        return self.cache[cache_key]  # Instantáneo!

    # Si no está en cache, procesar normal
    result = self._process_query(question)

    # Guardar en cache
    self.cache[cache_key] = result
    return result
```

**Casos de uso del cache:**
- Preguntas frecuentes (FAQ)
- Dashboards que refrescan cada minuto
- Queries de múltiples usuarios (misma pregunta)

**Limitaciones del cache:**
- Solo funciona para queries EXACTAMENTE iguales
- Requiere memoria (en producción usar Redis)
- Cache puede desactualizarse si cambias documentos

**💡 Práctica:**
> "Probemos con una variación de la query..."

```python
# Query ligeramente diferente
result3 = rag_v2.query("¿Cuál es la política de vacaciones?")  # Sin ? final
# → NO usa cache (string diferente)
```

**Solución avanzada (mencionar brevemente):**
```python
# Normalizar queries antes de cachear
def normalize_query(q):
    return q.lower().strip().rstrip('?!.')

cache_key = hashlib.md5(normalize_query(question).encode()).hexdigest()
```

#### 5. Re-ranking Semántico (10 min) ⭐ CORE FEATURE

**Instructor ejecuta Celda 9:**

```python
query = "beneficios para empleados senior"

# Sin re-ranking (v1)
results_v1 = rag_v1.search(query, k=5)

# Con re-ranking (v2)
results_v2 = rag_v2.search_with_rerank(query, k=5)
```

**Comparar resultados:**

**Sin re-ranking:**
```
Chunk 1: "...beneficios incluyen seguro médico, dental y visión..."
Chunk 2: "...empleados senior con más de 5 años tienen acceso..."
Chunk 3: "...la cafetería ofrece descuentos para empleados..."
```

**Con re-ranking:**
```
Chunk 1: "...empleados senior con más de 5 años tienen acceso..." (Score: 0.892)
Chunk 2: "...beneficios adicionales para senior: bonos anuales..." (Score: 0.845)
Chunk 3: "...beneficios incluyen seguro médico, dental y visión..." (Score: 0.723)
```

**Explicar algoritmo de re-ranking:**

```python
def rerank_results(query, results, weights=None):
    """
    Combina múltiples señales:
    1. Similitud semántica (embedding similarity) - 40%
    2. Keyword matching (BM25-like) - 25%
    3. Position bias (chunks tempranos) - 10%
    4. Length preference (chunks completos) - 10%
    5. Metadata signals (relevancia de sección) - 15%
    """

    scores = []
    for doc in results:
        # Señal 1: Embedding similarity (ya calculado)
        semantic_score = doc['distance']

        # Señal 2: Keyword matching
        keywords = extract_keywords(query)
        keyword_score = sum(1 for kw in keywords if kw in doc['text']) / len(keywords)

        # Señal 3: Position (primeros chunks son más importantes)
        position_score = 1 / (1 + doc['position'] / 10)

        # Señal 4: Length (preferir chunks completos)
        length_score = min(len(doc['text']) / 1000, 1.0)

        # Señal 5: Metadata (ejemplo: sección "benefits" más relevante)
        metadata_score = 1.0 if doc.get('section') == 'benefits' else 0.5

        # Score final ponderado
        final_score = (
            semantic_score * 0.40 +
            keyword_score * 0.25 +
            position_score * 0.10 +
            length_score * 0.10 +
            metadata_score * 0.15
        )

        scores.append(final_score)

    # Re-ordenar por score
    sorted_results = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    return sorted_results
```

**💡 Valor del re-ranking:**
- Mejora precisión 15-20%
- Especialmente útil cuando embedding similarity no es suficiente
- Combina lo mejor de búsqueda semántica + keyword

**Cuándo NO usar re-ranking:**
- Si latencia es crítica (añade ~100-200ms)
- Si los resultados de embedding ya son muy buenos
- Si no tienes suficientes señales adicionales

#### 6. Metadatos Enriquecidos (7 min)

**Mostrar ejemplo de chunk con metadatos:**

```python
{
    'id': 'chunk_42',
    'text': 'Los empleados senior con más de 5 años...',
    'metadata': {
        'source': 'company_handbook.pdf',
        'page': 15,
        'section': 'benefits',
        'subsection': 'senior_benefits',
        'chunk_position': 42,
        'char_count': 987,
        'word_count': 156,
        'has_numbers': True,
        'has_lists': True,
        'created_at': '2025-01-15T10:30:00Z',
        'hash': 'a3f2b8c...'
    }
}
```

**Usos de metadatos:**

1. **Filtrado:**
```python
# Solo chunks de la sección de beneficios
results = collection.query(
    query_texts=["vacaciones"],
    where={"section": "benefits"}
)
```

2. **Citación de fuentes:**
```python
# Incluir en la respuesta
answer = f"{response}\n\nFuente: {metadata['source']}, página {metadata['page']}"
```

3. **Deduplicación:**
```python
# Evitar chunks duplicados por overlap
seen_hashes = set()
unique_results = [r for r in results if r['hash'] not in seen_hashes and not seen_hashes.add(r['hash'])]
```

4. **Analytics:**
```python
# Qué secciones se consultan más
section_stats = Counter(r['metadata']['section'] for r in all_queries)
```

---

### PARTE 3: Optimización de Prompts [11:30-11:45] - 15 min

#### 7. Comparar Prompts (7 min)

**Instructor ejecuta Celda 11:**

**Prompt básico (Módulo 1):**
```python
prompt_v1 = """
Contexto: {context}
Pregunta: {question}
Responde basándote en el contexto.
"""
# 76 tokens
```

**Prompt optimizado (Módulo 2):**
```python
prompt_v2 = """
Eres un asistente experto en recursos humanos analizando documentos de la empresa.

CONTEXTO RELEVANTE:
{context}

PREGUNTA DEL EMPLEADO:
{question}

INSTRUCCIONES:
1. Responde ÚNICAMENTE basándote en el contexto proporcionado
2. Si la información está incompleta, indícalo claramente
3. Usa bullet points para listas
4. Sé específico con números y fechas
5. Máximo 3-4 oraciones para respuestas simples

RESPUESTA:
"""
# 142 tokens
```

**Diferencias clave:**

| Aspecto | Prompt Básico | Prompt Optimizado |
|---------|--------------|-------------------|
| **Rol** | No definido | "Asistente experto en RH" |
| **Estructura** | Plana | Secciones claras (CONTEXTO, PREGUNTA, INSTRUCCIONES) |
| **Restricciones** | Vago ("basándote en contexto") | Específico ("ÚNICAMENTE", "máximo 3-4 oraciones") |
| **Formato** | No especificado | "Bullet points para listas" |
| **Manejo de edge cases** | No contempla | "Si info incompleta, indícalo" |
| **Tokens** | 76 | 142 (+87% más largo) |

**⚠️ Trade-off importante:**
- Prompt más largo = más tokens = más costo
- Pero mejora calidad significativamente
- En este caso: +87% tokens, pero +15% accuracy → Vale la pena

**Mostrar resultados comparativos:**

```python
# Misma query con ambos prompts
query = "¿Cuál es la política de trabajo remoto?"

# Con prompt básico
"La empresa permite trabajo remoto 2 días a la semana."

# Con prompt optimizado
"Política de Trabajo Remoto:
• Empleados pueden trabajar remotamente hasta 2 días/semana
• Requiere aprobación previa del manager
• Debe mantener disponibilidad en horario laboral (9 AM - 6 PM)

Nota: Esta política aplica solo para roles elegibles (ver manual, pág. 23)"
```

**Mejor estructura, más detalle, incluye source.**

#### 8. Experimentar con Temperature (8 min)

**Instructor ejecuta Celda 12:**

```python
query = "¿Cuáles son los beneficios de la empresa?"
temperatures = [0.0, 0.3, 0.7, 1.0]

for temp in temperatures:
    rag_v2.temperature = temp
    result = rag_v2.query(query)
    print(f"🌡️ Temp {temp}: {result['response'][:150]}...")
```

**Resultados esperados:**

**Temperature 0.0 (Determinístico):**
```
Los beneficios incluyen:
- Seguro médico, dental y de visión
- 401(k) con 4% de matching
- 22 días de vacaciones
- Licencia parental pagada
```
*Siempre la misma respuesta, palabra por palabra*

**Temperature 0.3 (Recomendado):**
```
La empresa ofrece los siguientes beneficios:
• Cobertura médica completa (salud, dental, visión)
• Plan de retiro 401(k) con aporte de 4%
• 22 días hábiles de vacaciones anuales
• Licencia parental de 12 semanas pagadas
```
*Ligeramente diferente cada vez, pero consistente en contenido*

**Temperature 0.7 (Creativo):**
```
¡Tenemos excelentes beneficios! Destacan nuestro robusto seguro médico
que cubre todo, un generoso 401(k) donde la empresa aporta hasta 4%,
vacaciones abundantes (22 días!), y una política parental líder en la industria.
```
*Más variación, tono más conversacional*

**Temperature 1.0 (Muy creativo):**
```
Nuestro paquete de beneficios es excepcional. Imagina tener tranquilidad
total con seguro médico premium, construir tu futuro con 401(k) generoso,
disfrutar de casi un mes de vacaciones, y además...
```
*Mucha variación, puede divagar*

**Tabla comparativa:**

| Temperature | Variación | Tono | Adherencia al Contexto | Recomendado Para |
|-------------|-----------|------|------------------------|------------------|
| 0.0 | Ninguna | Robótico | 100% | Respuestas técnicas exactas |
| 0.3 | Mínima | Natural | 98% | **RAG general (ÓPTIMO)** |
| 0.7 | Media | Conversacional | 90% | Chatbots creativos |
| 1.0 | Alta | Muy libre | 75% | Escritura creativa |

**💡 Recomendación:**
> "Para RAG, temperature 0.3 es el sweet spot. Suficiente variación para sonar natural, pero muy adherente al contexto. Temperature alta (0.7-1.0) aumenta riesgo de alucinaciones."

---

### PARTE 4: Métricas y Comparación Final [11:45-12:05] - 20 min

#### 9. Benchmark Completo (12 min)

**Instructor ejecuta Celda 14:**

```python
test_queries = [
    "¿Cuál es la política de vacaciones?",
    "¿Qué beneficios tienen los empleados senior?",
    "¿Cómo funciona el trabajo remoto?",
    "¿Cuál es el proceso de onboarding?"
]

results_comparison = []

for query in test_queries:
    # Módulo 1
    result_v1 = rag_v1.query(query)
    time_v1 = ...
    eval_v1 = TestSuite.evaluate_response(result_v1, Module.BASICS)

    # Módulo 2
    result_v2 = rag_v2.query(query)
    time_v2 = ...
    eval_v2 = TestSuite.evaluate_response(result_v2, Module.OPTIMIZED)

    results_comparison.append({...})
```

**Resultados típicos:**

| Query | V1 Time | V2 Time | V1 Score | V2 Score | Speedup |
|-------|---------|---------|----------|----------|---------|
| Política vacaciones | 1,923ms | 1,045ms | 0.72 | 0.85 | 1.84x |
| Beneficios senior | 2,134ms | 987ms | 0.68 | 0.82 | 2.16x |
| Trabajo remoto | 1,845ms | 1,123ms | 0.75 | 0.88 | 1.64x |
| Proceso onboarding | 2,087ms | 1,234ms | 0.71 | 0.79 | 1.69x |
| **PROMEDIO** | **1,997ms** | **1,097ms** | **0.72** | **0.84** | **1.83x** |

**Análisis de mejoras:**
```
📈 MEJORAS PROMEDIO:
⏱️ Latencia: 1,997ms → 1,097ms (1.8x más rápido, -45%)
🎯 Calidad: 0.72 → 0.84 (+0.12, +17%)
```

**⭐ Cumplimos targets:**
- ✅ Latencia: Target era 1,000ms, logramos 1,097ms (muy cerca)
- ✅ Calidad: Target era 0.80, logramos 0.84 (superado)

#### 10. Visualizar Mejoras (8 min)

**Instructor ejecuta Celda 15 (gráficos):**

**Gráfico 1: Reducción de Latencia**
- Barras: Módulo 1 (rojo) vs Módulo 2 (verde)
- Flecha verde mostrando mejora de -45%
- Línea de objetivo (1,000ms)

**Gráfico 2: Mejora en Calidad**
- Barras mostrando score 0.72 → 0.84
- Destacar que superamos el target de 0.80

**Gráfico 3: Breakdown de Tiempos**
- Módulo 1: Retrieval (800ms) + Generation (1,200ms) + Cache (0ms)
- Módulo 2: Retrieval (600ms) + Generation (400ms) + Cache (50ms) + Rerank (50ms)

**Explicar cada optimización:**

```
📊 Breakdown de optimizaciones:

Retrieval: 800ms → 600ms (-200ms)
  • Chunks más grandes = menos chunks = menos búsquedas

Generation: 1,200ms → 400ms (-800ms) 🏆 MAYOR MEJORA
  • Cache hits ahorran 90% del tiempo
  • Prompt optimizado genera respuestas más concisas

Nuevos componentes:
  • Cache lookup: +50ms (pero ahorra 1,200ms cuando hit)
  • Re-ranking: +50ms (pero mejora accuracy 15%)
```

**💡 Lección clave:**
> "El cache es el componente con mayor ROI. Un cache hit ahorra 1,200ms y solo cuesta 50ms de lookup. Por eso en producción siempre usen cache (Redis, Memcached)."

---

### PARTE 5: Ejercicios Prácticos [12:05-12:15] - 10 min

**Instructor presenta los 3 ejercicios (Celdas 17-19):**

#### Ejercicio 1: Optimizar chunk_size (3 min)

**Instructor explica:**
> "Probamos 500 y 1000. ¿Cuál es el tamaño óptimo? Experimenten con [300, 500, 800, 1000, 1500, 2000]"

**Estructura sugerida:**
```python
chunk_sizes = [300, 500, 800, 1000, 1500, 2000]
results = []

for size in chunk_sizes:
    rag_v2.chunk_size = size
    chunks = rag_v2.create_chunks(doc)
    rag_v2.index_chunks(chunks[:30])

    result = rag_v2.query("¿Cuál es la política de vacaciones?")
    results.append({
        'size': size,
        'latency': result['metrics']['total_time_ms'],
        'quality': TestSuite.evaluate_response(result['response'], Module.OPTIMIZED)['score']
    })

# Graficar latencia vs quality
```

**Respuesta esperada:**
- Chunks muy pequeños (300): Muchos chunks, slow retrieval, contexto fragmentado
- **Chunks medianos (800-1000): Balance óptimo** ⭐
- Chunks muy grandes (2000): Pocos chunks, contexto diluido

#### Ejercicio 2: Filtrado por Metadatos (3 min)

**Instructor explica:**
> "Implementen una función que filtre resultados por sección del documento"

**Solución básica:**
```python
def filter_by_metadata(results, filter_criteria):
    filtered = []
    for result in results:
        match = True
        for key, value in filter_criteria.items():
            if result['metadata'].get(key) != value:
                match = False
                break
        if match:
            filtered.append(result)
    return filtered

# Uso
filter_criteria = {"section": "benefits"}
filtered_results = filter_by_metadata(results, filter_criteria)
```

#### Ejercicio 3: Prompt Técnico Especializado (4 min)

**Instructor muestra ejemplo:**

```python
technical_prompt = """
Eres un especialista en soporte técnico IT analizando documentación técnica corporativa.

DOCUMENTACIÓN RELEVANTE:
{context}

CONSULTA TÉCNICA:
{question}

INSTRUCCIONES:
1. Proporciona SOLO información basada en la documentación
2. Si requiere configuración, usa formato de código:
   ```
   parámetro: valor
   ```
3. Incluye advertencias de seguridad si aplica
4. Si la info está incompleta, indica claramente qué falta
5. Estructura la respuesta así:
   - Respuesta directa (1-2 líneas)
   - Pasos de configuración (si aplica)
   - Notas adicionales

RESPUESTA TÉCNICA:
"""

# Probar con query técnica
rag_v2.prompt_template = technical_prompt
result = rag_v2.query("¿Cómo configuro el VPN de la empresa?")
```

**Salida esperada:**
```
Para configurar el VPN corporativo:

PASOS:
1. Descarga el cliente Cisco AnyConnect desde el portal IT
2. Configuración:
   ```
   Server: vpn.techcorp.com
   Port: 443
   Protocol: SSL
   ```
3. Credenciales: Usa tu usuario corporativo + token MFA

⚠️ SEGURIDAD: Nunca uses VPN desde redes públicas sin verificar el certificado SSL primero.

Nota: Para troubleshooting, contacta IT Help Desk (ext. 5500).
```

**Comparar con prompt genérico** para mostrar la diferencia.

---

## 🎉 Cierre del Módulo [12:10-12:15] - 5 min

**Instructor ejecuta Celda 20 y resume:**

### ✅ Lo que lograron:

1. **Chunking con Overlap** → Mejor preservación de contexto (+25% cobertura)
2. **Caching Inteligente** → Respuestas instantáneas (12x speedup)
3. **Re-ranking** → Resultados más relevantes (+15% accuracy)
4. **Prompts Optimizados** → Respuestas más precisas y estructuradas
5. **Metadatos Enriquecidos** → Mejor trazabilidad y filtrado

### 📊 Mejoras Conseguidas:

| Métrica | Módulo 1 | Módulo 2 | Mejora | Target |
|---------|----------|----------|--------|--------|
| Latencia | 2000ms | 1100ms | **-45%** | -50% ✅ |
| Costo | $0.010 | $0.008 | **-20%** | -20% ✅ |
| Calidad | 0.70 | 0.84 | **+20%** | +10% ✅✅ |

**Superamos todos los targets!**

### 🚀 Próximo: Módulo 3 - Frameworks Avanzados

**Instructor explica:**
> "Hasta ahora hemos construido todo desde cero para entender los fundamentos. En Módulo 3 usaremos frameworks profesionales:
> - **LangChain:** Para pipelines complejos y agents
> - **LlamaIndex:** Para indexación avanzada y multi-document
> - **LangGraph:** Para workflows con estado
> - **Evaluación:** Para medir calidad objetivamente"

**Transición:**
> "¡Break de 15 minutos! Nos vemos en el Módulo 3 a las 12:30\. Aprovechen para:
> - Experimentar con los ejercicios
> - Revisar las soluciones en `/solutions/nivel_2_workshop/`
> - Pensar en su caso de uso específico"

---

## 📊 Métricas de Éxito del Módulo

Al final del módulo, verificar:

- [ ] **90%+** implementaron chunking con overlap exitosamente
- [ ] **90%+** vieron mejora de latencia con cache
- [ ] **80%+** entienden cómo funciona re-ranking
- [ ] **100%** ejecutaron benchmark comparativo
- [ ] **Promedio grupal:** Latencia < 1,200ms
- [ ] **Promedio grupal:** Accuracy > 0.78
- [ ] **Al menos 50%** intentaron los ejercicios prácticos

---

## 🚨 Problemas Comunes y Soluciones

### 1. Cache no funciona
**Síntomas:** Segunda query tarda igual que la primera
**Causas:**
- Query con diferente capitalización
- Espacio extra al inicio/final
- Signos de puntuación diferentes

**Solución:**
```python
# Verificar que las queries son idénticas
q1 = "¿Cuál es la política de vacaciones?"
q2 = "¿Cuál es la política de vacaciones?"
print(q1 == q2)  # Debe ser True

# Si no funciona, revisar implementación del cache
print(rag_v2.cache.keys())  # Ver qué queries están cacheadas
```

### 2. Overlap genera chunks duplicados en resultados
**Síntomas:** Misma información aparece 2-3 veces en la respuesta
**Causa:** Chunks solapados son muy similares

**Solución:**
```python
# Deduplicación por hash
def deduplicate_results(results):
    seen_hashes = set()
    unique = []
    for r in results:
        content_hash = hashlib.md5(r['text'].encode()).hexdigest()
        if content_hash not in seen_hashes:
            unique.append(r)
            seen_hashes.add(content_hash)
    return unique
```

### 3. Re-ranking empeora resultados
**Síntomas:** Score baja en vez de subir
**Causa:** Pesos mal balanceados

**Solución:**
```python
# Experimentar con diferentes pesos
weights = {
    'semantic': 0.60,  # Aumentar si embeddings son buenos
    'keyword': 0.20,   # Reducir si muchos false positives
    'position': 0.05,
    'length': 0.05,
    'metadata': 0.10
}

results = rag_v2.search_with_rerank(query, weights=weights)
```

### 4. Latencia no mejora
**Síntomas:** Módulo 2 igual de lento que Módulo 1
**Causas:**
- Cache deshabilitado
- Queries siempre diferentes (no hits de cache)
- Chunks muy grandes

**Debug:**
```python
# Verificar cache
print(f"Cache enabled: {rag_v2.cache_enabled}")
print(f"Cache size: {len(rag_v2.cache)}")
print(f"Cache hit rate: {rag_v2.cache_hits / (rag_v2.cache_hits + rag_v2.cache_misses)}")

# Verificar tamaño de chunks
print(f"Average chunk size: {np.mean([len(c) for c in chunks_v2])}")
```

### 5. Prompts optimizados son demasiado caros
**Síntomas:** Costo se dispara por prompts largos
**Solución:**
```python
# Prompt medio: más corto que optimizado, mejor que básico
prompt_medium = """
Eres un asistente de RH. Usa SOLO el contexto para responder.

CONTEXTO: {context}
PREGUNTA: {question}

Respuesta concisa con bullets si aplica:
"""
# ~60 tokens (vs 142 del optimizado, 76 del básico)
```

---

## 💡 Tips de Enseñanza

### Timing Crítico
- **No extender más de 90 min:** El módulo es denso
- **Almuerzo a tiempo:** Participantes necesitan el break
- **Si van atrasados:** Saltear ejercicios, dejarlos para después del almuerzo

### Demos Efectivas
- **Cache:** Hacer la demo en vivo, mostrar la diferencia de tiempo
- **Re-ranking:** Mostrar side-by-side con y sin re-ranking
- **Temperature:** Ejecutar múltiples veces con temp=1.0 para mostrar variación

### Engagement
- **Celebrar mejoras:** "¡Miren, 45% más rápido!"
- **Competencia amistosa:** "¿Quién logró mayor speedup?"
- **Casos reales:** Pedir a participantes que piensen cómo aplicarían cache en su contexto

### Ejercicios
- **No esperar que todos terminen:** 10 min es poco, es exploración inicial
- **Soluciones disponibles:** Recordar que están en `/solutions/nivel_2_workshop/`
- **Para casa:** Si no terminan, pueden continuar después

---

## 📚 Recursos Adicionales

### Compartir con participantes:
- [Chunking Strategies Deep Dive](https://www.pinecone.io/learn/chunking-strategies/)
- [Redis for Caching](https://redis.io/docs/manual/client-side-caching/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- Soluciones completas: `/solutions/nivel_2_workshop/`

### Lecturas avanzadas (post-workshop):
- [Hybrid Search (Dense + Sparse)](https://www.pinecone.io/learn/hybrid-search/)
- [Re-ranking Algorithms](https://www.sbert.net/examples/applications/cross-encoder/README.html)
- [Production RAG Patterns](https://eugeneyan.com/writing/llm-patterns/)

---

## ✅ Checklist del Instructor

**Antes del módulo:**
- [ ] Revisar soluciones en `/solutions/nivel_2_workshop/`
- [ ] Probar benchmark comparativo con datos reales
- [ ] Preparar ejemplos de prompts especializados
- [ ] Tener gráficos de mejoras listos

**Durante el módulo:**
- [ ] Demo de cache en vivo (Celda 8)
- [ ] Mostrar re-ranking side-by-side (Celda 9)
- [ ] Ejecutar benchmark completo (Celda 14)
- [ ] Mostrar visualizaciones (Celda 15)
- [ ] Presentar los 3 ejercicios (Celdas 17-19)

**Después del módulo:**
- [ ] Recopilar métricas grupales (latencia, accuracy promedio)
- [ ] Identificar optimizaciones que generaron más impacto
- [ ] Anotar preguntas frecuentes para próximas ediciones
- [ ] Verificar que participantes tienen acceso a soluciones

---

**🚀 ¡Éxito con el módulo más técnico del día!**
