# 📚 Soluciones Completas - Notebook 02: Arquitectura y Optimización

**Nivel 2: Workshop** - Soluciones esperadas durante el workshop

---

## 📋 Índice de Soluciones

### ✅ Ejercicios Principales (Celdas 17-19)

| # | Archivo | Celda | Descripción | Líneas | Dificultad |
|---|---------|-------|-------------|--------|------------|
| 1 | `02_solucion_ejercicio1.py` | 17 | Optimizar chunk_size | 89 | ⭐⭐ Media |
| 2 | `02_solucion_ejercicio2.py` | 18 | Filtrado por metadata | 83 | ⭐⭐ Media |
| 3 | `02_solucion_ejercicio3.py` | 19 | Prompt especializado técnico | 82 | ⭐⭐ Media |
| 4 | `02_solucion_ejercicio4_temperaturas.py` | 8 | Experimentar con temperaturas | 147 | ⭐⭐ Media |

### 🏆 Desafíos Adicionales (Celda 18 del notebook)

| # | Archivo | Descripción | Líneas | Dificultad |
|---|---------|-------------|--------|------------|
| 5 | `02_solucion_desafio_smart_chunking.py` | Chunking inteligente | 289 | ⭐⭐⭐ Alta |
| 6 | `02_solucion_desafio_metadata_indexing.py` | Indexación con metadata | 437 | ⭐⭐⭐ Alta |
| 7 | `02_solucion_desafio_reranking.py` | Re-ranking avanzado | 394 | ⭐⭐⭐ Alta |

**Total**: 7 soluciones completas | 1,331 líneas de código

---

## 🎯 Ejercicio 1: Optimizar chunk_size

**Archivo**: `02_solucion_ejercicio1.py`
**Celda del notebook**: 17
**Tiempo estimado**: 15-20 minutos

### Objetivo
Encontrar el chunk_size óptimo probando diferentes tamaños y midiendo el balance entre latencia y calidad.

### Conceptos aprendidos
- ✅ Experimentación sistemática con parámetros
- ✅ Trade-offs entre tamaño de chunk y performance
- ✅ Métricas combinadas (calidad/latencia)
- ✅ Análisis de resultados con pandas

### Snippet clave
```python
for size in chunk_sizes:
    rag.chunk_size = size
    chunks = rag.create_chunks(doc)

    # Medir latencia y calidad
    times, scores = [], []
    for query in test_queries:
        start = time.time()
        response = rag.query(query)
        times.append((time.time() - start) * 1000)

        eval_result = TestSuite.evaluate_response(response['response'])
        scores.append(eval_result['score'])

    # Score combinado
    combined_score = avg_score / (avg_time / 1000)
```

### Output esperado
```
📊 RESULTADOS COMPARATIVOS:
chunk_size  num_chunks  avg_latency_ms  avg_quality  combined_score
300         67          850             0.72         0.847
500         40          920             0.78         0.848
800         25          1050            0.82         0.781  ← Mejor balance
1000        20          1100            0.80         0.727
```

---

## 🎯 Ejercicio 2: Filtrado por metadata

**Archivo**: `02_solucion_ejercicio2.py`
**Celda del notebook**: 18
**Tiempo estimado**: 15 minutos

### Objetivo
Implementar función de filtrado de resultados basado en metadata (sección, tipo de contenido, etc.)

### Conceptos aprendidos
- ✅ Metadata enriquecidos en vectorDB
- ✅ Filtrado programático de resultados
- ✅ Mejora de precisión con filtros
- ✅ Type hints y documentación

### Snippet clave
```python
def filter_by_metadata(results: Dict, filter_criteria: Dict[str, Any]) -> Dict:
    filtered_docs, filtered_metadata, filtered_scores = [], [], []

    for i, metadata in enumerate(results.get('metadatas', [])):
        match = all(
            metadata.get(key) == value
            for key, value in filter_criteria.items()
        )

        if match:
            filtered_docs.append(results['documents'][i])
            filtered_metadata.append(metadata)
            if 'scores' in results:
                filtered_scores.append(results['scores'][i])

    return {
        'documents': filtered_docs,
        'metadatas': filtered_metadata,
        'scores': filtered_scores
    }
```

### Output esperado
```
📊 Resultados sin filtro: 10 documentos
🔧 Aplicando filtro: {"section": "benefits"}
📊 Resultados filtrados: 3 documentos

✅ Top 3 resultados filtrados:
1. Los empleados reciben seguro médico completo...
   Metadata: {'section': 'benefits', 'chunk_id': 5}
```

---

## 🎯 Ejercicio 3: Prompt especializado técnico

**Archivo**: `02_solucion_ejercicio3.py`
**Celda del notebook**: 19
**Tiempo estimado**: 10-15 minutos

### Objetivo
Diseñar un prompt optimizado para queries técnicas con formato estructurado.

### Conceptos aprendidos
- ✅ Ingeniería de prompts
- ✅ Definición de roles específicos
- ✅ Formato de salida estructurado
- ✅ Mejora de calidad de respuestas

### Snippet clave
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
4. Estructura: Respuesta directa → Pasos → Notas

RESPUESTA TÉCNICA:
"""
```

### Output esperado
```
Query: ¿Cómo configuro el VPN de la empresa?

Con prompt técnico:
✅ Respuesta estructurada
✅ Pasos numerados claramente
✅ Código/configuración resaltada
✅ Advertencias de seguridad incluidas

Con prompt genérico:
❌ Respuesta narrativa sin estructura
❌ Sin diferenciación de código
```

---

## 🎯 Ejercicio 4: Experimentar con temperaturas

**Archivo**: `02_solucion_ejercicio4_temperaturas.py`
**Celda del notebook**: 8 (Experimentación extendida)
**Tiempo estimado**: 20 minutos

### Objetivo
Probar diferentes temperaturas del LLM para encontrar el valor óptimo para RAG.

### Conceptos aprendidos
- ✅ Impacto de la temperatura en respuestas
- ✅ Balance determinismo vs naturalidad
- ✅ Medición de consistencia
- ✅ Configuración óptima para casos de uso

### Snippet clave
```python
temperatures = [0.0, 0.3, 0.5, 0.7, 1.0]

for temp in temperatures:
    rag.temperature = temp

    # Ejecutar misma query múltiples veces
    responses = [rag.query(question) for _ in range(3)]

    # Medir variabilidad
    lengths = [len(r['response']) for r in responses]
    variability = max(lengths) - min(lengths)

    # Word overlap entre respuestas
    words_sets = [set(r['response'][:100].split()) for r in responses]
    overlap = len(words_sets[0] & words_sets[1]) / len(words_sets[0])
```

### Output esperado
```
🌡️ TEMPERATURA: 0.0
   Variabilidad: 0 chars, 100% palabra overlap
   ✅ Perfecto para queries factuales

🌡️ TEMPERATURA: 0.3
   Variabilidad: 15 chars, 95% palabra overlap
   ✅ RECOMENDADO para RAG - Balance ideal

🌡️ TEMPERATURA: 1.0
   Variabilidad: 150 chars, 60% palabra overlap
   ⚠️  Muy variable - Riesgo de alucinaciones
```

---

## 🏆 Desafío 5: Smart Chunking

**Archivo**: `02_solucion_desafio_smart_chunking.py`
**Dificultad**: ⭐⭐⭐ Alta
**Tiempo estimado**: 30-40 minutos

### Objetivo
Implementar chunking inteligente que respeta límites de frases y párrafos, con overlap.

### Técnicas avanzadas
- ✅ Regex para detectar límites de frases
- ✅ Preservación de contexto con overlap adaptativo
- ✅ Manejo de frases muy largas
- ✅ Algoritmo de ventana deslizante

### Snippet clave
```python
def smart_chunking(text: str, chunk_size: int = 500, overlap: int = 100):
    # Dividir en frases respetando puntuación
    sentence_endings = r'[.!?]\s+|\n\n'
    sentences = re.split(sentence_endings, text)

    chunks = []
    current_chunk = ""
    previous_overlap = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size:
            # Guardar chunk con overlap
            full_chunk = previous_overlap + " " + current_chunk
            chunks.append(full_chunk.strip())

            # Calcular overlap para siguiente chunk
            words = current_chunk.split()
            overlap_words = []
            overlap_chars = 0

            for word in reversed(words):
                if overlap_chars + len(word) < overlap:
                    overlap_words.insert(0, word)
                    overlap_chars += len(word) + 1
                else:
                    break

            previous_overlap = " ".join(overlap_words)
            current_chunk = sentence
        else:
            current_chunk += " " + sentence

    return chunks
```

### Beneficios
```
✅ Preserva significado completo de frases
✅ Mejora comprensión del contexto
✅ Reduce fragmentación de información
✅ Facilita retrieval semántico más preciso

🎯 Ideal para:
   - Documentos técnicos con procedimientos
   - Manuales con instrucciones paso a paso
   - FAQs donde cada Q&A es una unidad
```

---

## 🏆 Desafío 6: Metadata Enriquecidos

**Archivo**: `02_solucion_desafio_metadata_indexing.py`
**Dificultad**: ⭐⭐⭐ Alta
**Tiempo estimado**: 40-50 minutos

### Objetivo
Implementar sistema de metadata enriquecidos para chunks con múltiples señales de calidad.

### Metadata implementados
1. **Básicos**: chunk_id, source_document, position
2. **Contenido**: length, section, content_type
3. **Técnicos**: content_hash, indexed_at, version
4. **Calidad**: completeness_score, info_density

### Snippet clave
```python
def extract_metadata_from_chunk(chunk, chunk_id, source_doc, total_chunks):
    metadata = {
        # Básicos
        'chunk_id': chunk_id,
        'source_document': Path(source_doc).name,
        'chunk_position': f"{chunk_id + 1}/{total_chunks}",

        # Contenido
        'section': detect_section(chunk),  # benefits, vacation, etc.
        'content_type': detect_content_type(chunk),  # list, table, narrative

        # Calidad
        'completeness_score': calculate_completeness(chunk),  # 0-1
        'info_density': calculate_info_density(chunk),  # 0-1

        # Técnicos
        'content_hash': hashlib.md5(chunk.encode()).hexdigest(),
        'indexed_at': datetime.now().isoformat(),
    }
    return metadata
```

### Casos de uso
```
1️⃣ FILTRADO AVANZADO:
   - Buscar solo en sección 'benefits'
   - Excluir chunks con baja info_density
   - Filtrar por tipo de contenido

2️⃣ RE-RANKING MEJORADO:
   - Priorizar chunks con alta completeness
   - Boost a secciones específicas
   - Penalizar chunks incompletos

3️⃣ TRAZABILIDAD:
   - Saber exactamente de dónde viene info
   - Tracking de versiones
   - Auditoría de uso

4️⃣ ANALYTICS:
   - Qué secciones se consultan más
   - Gaps en documentación
   - Calidad de la base de conocimiento
```

---

## 🏆 Desafío 7: Re-ranking Avanzado

**Archivo**: `02_solucion_desafio_reranking.py`
**Dificultad**: ⭐⭐⭐ Alta
**Tiempo estimado**: 45-60 minutos

### Objetivo
Implementar sistema de re-ranking multi-señal para mejorar relevancia de resultados.

### Señales de ranking
1. **Semántico** (40%): Score original del embedding
2. **Keywords** (25%): Coincidencia exacta de términos
3. **Posición** (10%): Ubicación en el documento
4. **Longitud** (10%): Cercanía a longitud óptima
5. **Completitud** (15%): Frases completas

### Snippet clave
```python
def rerank_results(query, results, weights=None):
    if weights is None:
        weights = {
            'semantic': 0.40,
            'keyword': 0.25,
            'position': 0.10,
            'length': 0.10,
            'completeness': 0.15
        }

    reranked = []
    for result in results:
        # Calcular scores individuales
        keyword_score = calculate_keyword_score(query, result['text'])
        position_score = calculate_position_score(result['metadata']['chunk_id'])
        length_score = calculate_length_score(len(result['text']))
        completeness_score = calculate_completeness_score(result['text'])

        # Score final ponderado
        final_score = (
            result['score'] * weights['semantic'] +
            keyword_score * weights['keyword'] +
            position_score * weights['position'] +
            length_score * weights['length'] +
            completeness_score * weights['completeness']
        )

        result['rerank_score'] = final_score
        reranked.append(result)

    return sorted(reranked, key=lambda x: x['rerank_score'], reverse=True)
```

### Configuraciones pre-definidas
```python
configs = {
    'balanced': {
        'semantic': 0.40, 'keyword': 0.25, 'position': 0.10,
        'length': 0.10, 'completeness': 0.15
    },
    'keyword_focused': {
        'semantic': 0.30, 'keyword': 0.40, 'position': 0.05,
        'length': 0.10, 'completeness': 0.15
    },
    'quality_focused': {
        'semantic': 0.35, 'keyword': 0.20, 'position': 0.05,
        'length': 0.15, 'completeness': 0.25
    },
}
```

### Mejoras demostradas
```
✅ Penaliza chunks incompletos o mal formados
✅ Potencia matches exactos de keywords importantes
✅ Considera contexto del documento (posición)
✅ Mejora precision@3 en ~15-20%

Ejemplo:
Chunk incompleto "Seg" con score 0.78
→ Después de re-ranking: 0.45 (penalizado por completeness)

Chunk con keyword "senior" y score 0.80
→ Después de re-ranking: 0.88 (potenciado por keyword match)
```

---

## 🚀 Cómo usar estas soluciones

### Durante el workshop (Participantes)
```bash
# NO mirar las soluciones hasta intentar el ejercicio
# Si te atascas, pregunta al instructor primero

# Si necesitas un hint:
cat solutions/nivel_2_workshop/README_SOLUCIONES.md | grep "Snippet clave" -A 10
```

### Durante el workshop (Instructores)
```bash
# Mostrar solo el snippet relevante, no todo el archivo
# Explicar la lógica sin dar la solución completa
# Dejar que completen los detalles

# Para desbloquear rápido:
python solutions/nivel_2_workshop/02_solucion_ejercicio1.py
```

### Post-workshop (Estudio)
```bash
# Comparar tu solución con la esperada
diff mi_solucion.py solutions/nivel_2_workshop/02_solucion_ejercicio1.py

# Ejecutar todas las soluciones
for file in solutions/nivel_2_workshop/*.py; do
    echo "Ejecutando $file"
    python "$file"
done
```

---

## 📊 Métricas de aprendizaje

### Cobertura de conceptos

| Concepto | Ejercicio | Dificultad | Tiempo |
|----------|-----------|------------|--------|
| Experimentación sistemática | Ej 1 | Media | 20 min |
| Metadata filtering | Ej 2 | Media | 15 min |
| Prompt engineering | Ej 3 | Media | 15 min |
| LLM parameters | Ej 4 | Media | 20 min |
| Text processing avanzado | Desafío 5 | Alta | 40 min |
| Data enrichment | Desafío 6 | Alta | 50 min |
| Multi-signal ranking | Desafío 7 | Alta | 60 min |

**Total tiempo estimado**:
- Ejercicios principales: 70 minutos
- Desafíos adicionales: 150 minutos
- **Total**: 220 minutos (3h 40min)

### Progresión de dificultad
```
⭐⭐ Media (Ejercicios 1-4)
→ Conceptos fundamentales
→ Implementación guiada
→ Resultados inmediatos

⭐⭐⭐ Alta (Desafíos 5-7)
→ Conceptos avanzados
→ Implementación autónoma
→ Optimización y tuning
```

---

## 💡 Tips de aprendizaje

### Para maximizar el aprendizaje:

1. **Intenta primero sin mirar**: El error es parte del aprendizaje
2. **Lee los comentarios**: Explican el "por qué", no solo el "cómo"
3. **Modifica los parámetros**: Prueba valores diferentes
4. **Compara con tu solución**: ¿Qué mejoras puedes adoptar?
5. **Experimenta con tus datos**: Aplica a tu caso de uso real

### Para instructores:

1. **Nivel 1 (Desbloqueo rápido)**: Mostrar snippet clave
2. **Nivel 2 (Referencia)**: Ejecutar solución completa
3. **Nivel 3 (Profundización)**: Discutir trade-offs y alternativas

---

## 📚 Recursos adicionales

- [Documentación OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [ChromaDB Metadata Filtering](https://docs.trychroma.com/usage-guide#filtering-by-metadata)
- [Best Practices for Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)

---

**Última actualización**: 2025-10-01
**Autor**: Antonio Romero (aromero@secture.com)
**Workshop**: RAG 2025 - De Cero a Producción
