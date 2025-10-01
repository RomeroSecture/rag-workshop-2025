# 🎓 Guía del Instructor - Notebook 01: Fundamentos de RAG
## De Cero a tu Primer Sistema RAG Funcional

---

## 📋 Información General

**Duración:** 75 minutos (08:15-09:30)
**Objetivo:** Construir un sistema RAG funcional desde cero
**Nivel:** Fundamentos
**Pre-requisitos:** Haber completado Notebook 00 (setup verificado)

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este módulo, los participantes serán capaces de:

1. ✅ **Explicar** qué es RAG y sus 3 fases (Indexación, Retrieval, Generación)
2. ✅ **Implementar** un pipeline RAG completo en 50 líneas de código
3. ✅ **Cargar** documentos (PDF/TXT) y procesarlos
4. ✅ **Crear** chunks de texto efectivos
5. ✅ **Indexar** en una vector database (ChromaDB)
6. ✅ **Realizar** búsqueda semántica
7. ✅ **Generar** respuestas con contexto usando LLM
8. ✅ **Medir** latencia, costo y calidad

---

## 🗓️ Timeline Detallado

| Tiempo | Sección | Actividad | Celdas |
|--------|---------|-----------|--------|
| 00:00-00:20 | Parte 1: Teoría | Conceptos y arquitectura RAG | 1-4 |
| 00:20-00:40 | Parte 2: Implementación | Construir SimpleRAG | 5-9 |
| 00:40-01:15 | Parte 3: Práctica | Experimentos y optimización | 10-18 |

---

## 📝 Guión de la Sesión

### PARTE 1: Setup y Conceptos [08:15-08:35] - 20 min

#### 1. Introducción a RAG (5 min)

**Instructor presenta (Celda 1):**

> "RAG significa **Retrieval-Augmented Generation**. Es una técnica que combina:
> - 📚 Una base de conocimiento (tus documentos)
> - 🔍 Un buscador ultra-rápido (vector search)
> - 🤖 Un LLM (como GPT) para generar respuestas
>
> Es como darle a ChatGPT acceso a Google, pero solo sobre TUS documentos."

**Conceptos clave a enfatizar:**
- **Retrieval** = Buscar información relevante
- **Augmented** = Enriquecer el contexto del LLM
- **Generation** = Crear respuesta basada en contexto

**Ejecutar Celda 2:**
```python
import sys, os
from pathlib import Path
sys.path.append(str(Path.cwd().parent / 'src'))

from module_1_basics import Module1_BasicRAG
from shared_config import RAGMasterConfig, TestSuite, MetricsTracker, Module
```

**Salida esperada:**
```
✅ API Key configurada: sk-proj...
🚀 Ambiente listo para Módulo 1: Fundamentos
```

#### 2. Los 4 Pilares de RAG (7 min)

**Instructor ejecuta y explica Celda 4 (diagrama arquitectura):**

**El diagrama muestra 3 fases:**

**FASE 1: INDEXACIÓN** (preparar conocimiento)
```
📄 Documentos → ✂️ Text Splitter → 🔢 Embeddings → 💾 Vector DB
```

**Explicación paso a paso:**
- **Documentos Originales:** PDFs, TXTs, JSONs con tu conocimiento
- **Text Splitter:** Divide en chunks manejables (500-1000 chars)
- **Embeddings Model:** Convierte texto a vectores numéricos (arrays de 1536 dimensiones)
- **Vector Database:** Almacena vectores para búsqueda rápida

**FASE 2: RETRIEVAL** (buscar relevante)
```
❓ User Query → 🔢 Embed Query → 🔍 Semantic Search → 📑 Top-K Results
```

**Explicación:**
- **User Query:** "¿Cuál es la política de vacaciones?"
- **Embed Query:** Convertir pregunta a vector (mismo espacio que los documentos)
- **Semantic Search:** Calcular similitud coseno entre query y todos los chunks
- **Top-K Results:** Devolver los K chunks más similares (típicamente K=3-5)

**FASE 3: GENERACIÓN** (crear respuesta)
```
📑 Retrieved Context + ❓ Query → 🤖 LLM → 💬 Final Answer
```

**Explicación:**
- **Prompt Engineering:** Combinar contexto + pregunta en un prompt efectivo
- **LLM Generation:** GPT genera respuesta basándose SOLO en el contexto
- **Final Answer:** Respuesta fundamentada en tus documentos

**💡 Analogía útil:**
> "Es como buscar en un libro:
> 1. **Indexación** = Crear un índice del libro
> 2. **Retrieval** = Buscar en el índice las páginas relevantes
> 3. **Generación** = Leer esas páginas y resumir la respuesta"

#### 3. Métricas Clave (3 min)

**Instructor enfatiza las 3 métricas principales:**

| Métrica | Qué mide | Objetivo Módulo 1 |
|---------|----------|-------------------|
| **Latencia** | Tiempo de respuesta | < 2000ms |
| **Costo** | $ por query | < $0.01 |
| **Accuracy** | Calidad de respuesta | > 70% |

**Explicación:**
- **Latencia:** Suma de tiempo de retrieval (~500ms) + generación (~1500ms)
- **Costo:** Basado en tokens de entrada (context + query) y salida (respuesta)
- **Accuracy:** Evaluada con TestSuite.evaluate_response()

**💡 Insight:**
> "En producción, necesitas balance. Una respuesta perfecta (100% accuracy) que tarde 30 segundos no sirve. Buscaremos 90% accuracy en <1 segundo."

#### 4. Preguntas y Aclaraciones (5 min)

**Preguntas frecuentes esperadas:**

**P: "¿Por qué no simplemente pasarle todo el documento a GPT?"**
R: "GPT-3.5 tiene límite de ~4K tokens de contexto. Un documento típico tiene 50K+ tokens. Además, cuesta más y tarda más."

**P: "¿Los embeddings son caros de generar?"**
R: "No, text-embedding-3-small cuesta $0.00002 por 1K tokens. Indexar 100 páginas cuesta ~$0.20 total."

**P: "¿Qué tan buena es la búsqueda semántica?"**
R: "Muy buena. Encuentra 'días de descanso' cuando preguntas por 'vacaciones' porque entiende el significado, no solo keywords."

---

### PARTE 2: Implementación Básica [08:35-08:55] - 20 min

#### 5. Construyendo SimpleRAG (8 min)

**Instructor ejecuta Celda 6 explicando cada método:**

```python
class SimpleRAG:
    """Tu primer RAG en 50 líneas de código"""
```

**Método 1: __init__**
```python
def __init__(self):
    self.client = OpenAI(api_key=api_key)
    self.chroma = chromadb.Client()
    self.collection = self.chroma.create_collection("simple_rag")
```

**Explicar:**
- ChromaDB usa SQLite bajo el capó (no requiere servidor)
- La colección es como una tabla en SQL
- Si ya existe, se borra y recrea (modo desarrollo)

**Método 2: load_document**
```python
def load_document(self, filepath: str) -> str:
    # Soporta PDF y TXT
    if filepath.endswith('.pdf'):
        pdf = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() for page in pdf.pages)
```

**Explicar:**
- PyPDF2 extrae texto plano (sin imágenes/tablas)
- Para producción considerar: pdfplumber, pypdf, unstructured

**Método 3: create_chunks**
```python
def create_chunks(self, text: str, chunk_size: int = 500) -> List[str]:
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
```

**⚠️ Advertir limitaciones:**
- Este chunking es ingenuo (corta palabras/frases)
- En Módulo 2 mejoraremos con overlap y smart splitting
- Por ahora es suficiente para aprender el concepto

**Método 4: index_chunks**
```python
def index_chunks(self, chunks: List[str]):
    self.collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
```

**Explicar la "magia" de ChromaDB:**
- ChromaDB genera embeddings automáticamente
- Usa el modelo por defecto de Sentence Transformers
- No necesitas llamar a OpenAI embeddings (ahorra $)

**Método 5: query** (el más importante)
```python
def query(self, question: str, k: int = 3) -> str:
    # 1. Buscar chunks relevantes
    results = self.collection.query(
        query_texts=[question],
        n_results=k
    )

    # 2. Preparar contexto
    context = "\n\n".join(results['documents'][0])

    # 3. Generar respuesta
    prompt = f"""
    Contexto: {context}
    Pregunta: {question}
    Responde basándote ÚNICAMENTE en el contexto.
    """

    response = self.client.chat.completions.create(...)
```

**Explicar cada paso:**
1. **Retrieval:** ChromaDB hace vector search automáticamente
2. **Context Building:** Unimos los K chunks con saltos de línea
3. **Generation:** Prompt simple pero efectivo

**Métricas registradas:**
- Latencia de retrieval
- Latencia de generación
- Tokens usados
- Costo estimado

#### 6. Cargar Documento (4 min)

**Instructor ejecuta Celda 7:**

```python
doc_path = "../data/company_handbook.pdf"
text = rag.load_document(doc_path)
```

**Mostrar preview:**
```
📄 Cargando: ../data/company_handbook.pdf
✅ Documento cargado: 45,328 caracteres

📖 Preview del documento:
--------------------------------------------------
MANUAL DEL EMPLEADO

Bienvenido a TechCorp Inc.

Este manual contiene información importante sobre políticas...
```

**Explicar el contenido del documento:**
- Manual de empleado ficticio
- Contiene: políticas de vacaciones, beneficios, código de conducta, etc.
- Perfecto para queries tipo HR/RH

#### 7. Chunking e Indexación (4 min)

**Instructor ejecuta Celda 8:**

```python
chunks = rag.create_chunks(text, chunk_size=500)
```

**Salida típica:**
```
✂️ Creados 91 chunks de ~500 caracteres

📊 Estadísticas de chunking:
- Total chunks: 91
- Tamaño promedio: 498 chars
- Chunk más pequeño: 187 chars  # El último
- Chunk más grande: 500 chars
```

**Mostrar ejemplos de chunks (importante para debugging):**
```
Chunk 1:
----------------------------------------
MANUAL DEL EMPLEADO

Bienvenido a TechCorp Inc.

Este manual contiene información importante sobre políticas, beneficios y...

Chunk 2:
----------------------------------------
...y procedimientos de la empresa. Por favor, léelo cuidadosamente.

SECCIÓN 1: POLÍTICAS DE TRABAJO

1.1 Horario Laboral...
```

**⚠️ Señalar el problema:**
> "Vean que el Chunk 2 empieza con '...y procedimientos'. Esto pasa porque cortamos en mitad de una frase. Es un problema que resolveremos en Módulo 2 con overlap y smart chunking."

**Ejecutar Celda 9 (indexación):**

```python
chunks_to_index = chunks[:20]  # Solo primeros 20 para rapidez
rag.index_chunks(chunks_to_index)
```

**Salida:**
```
💾 PASO 2: INDEXACIÓN
==================================================
🎯 Indexando 20 chunks en ChromaDB...
✅ Indexación completada en 1,234ms
⚡ Velocidad: 16.2 chunks/segundo
```

**Explicar por qué solo 20 chunks:**
- Para que el workshop sea ágil
- En producción indexarías todos
- ChromaDB puede manejar millones de chunks

#### 8. Demo Rápida (4 min)

**Instructor hace una query en vivo:**

```python
# Query rápida para demostrar funcionamiento
respuesta = rag.query("¿Cuál es el horario de trabajo?")
```

**Mostrar el output completo:**
```
❓ Pregunta: ¿Cuál es el horario de trabajo?
🔍 Recuperados 3 chunks relevantes en 245ms
⏱️ Tiempos: Retrieval=245ms, Generation=1,567ms, Total=1,812ms

💬 Respuesta:
Según el manual, el horario de trabajo estándar es de 9:00 AM a 6:00 PM,
de lunes a viernes, con una hora de almuerzo.
```

**Explicar el flujo:**
1. Query convertida a embedding (automático por ChromaDB)
2. Búsqueda de 3 chunks más similares (245ms)
3. Chunks enviados a GPT como contexto
4. GPT genera respuesta basada en contexto (1,567ms)

---

### PARTE 3: Práctica - Tu Turno [08:55-09:30] - 35 min

#### 9. Primera Query Guiada (5 min)

**Instructor ejecuta Celda 11 paso a paso:**

```python
respuesta = rag.query("¿Cuál es la política de vacaciones?")
```

**Evaluación automática:**
```python
evaluation = TestSuite.evaluate_response(respuesta, Module.BASICS)
```

**Salida esperada:**
```
📊 Evaluación:
- Score: 0.75/1.0
- ¿Pasó?: ✅ Sí
- Tiene info básica: ✅
```

**Explicar cómo funciona la evaluación:**
- Verifica si contiene keywords esperadas (ej: "días", "vacaciones", "22")
- Verifica longitud mínima (>50 chars)
- Verifica que no dice "no sé" o "no tengo información"

**Si score < 0.7:**
- Puede ser que los chunks relevantes no estén en los 20 indexados
- Re-indexar más chunks: `rag.index_chunks(chunks[:50])`

#### 10. Experimentar con Diferentes Queries (8 min)

**Instructor ejecuta Celda 12:**

**Queries de prueba:**
1. "¿Cuál es el horario de trabajo?" → Debería responder bien
2. "¿Hay trabajo remoto?" → Debería responder bien
3. "¿Cuáles son los beneficios?" → Debería listar varios
4. "¿Cómo es el proceso de onboarding?" → Puede ser limitado si no indexamos esa parte
5. "¿Qué pasa si me caso?" → Edge case interesante

**Para cada query mostrar:**
- La respuesta generada
- El tiempo de ejecución
- Brevemente analizar si es correcta

**💡 Insight para compartir:**
> "Vean que queries 1-3 funcionan bien porque probablemente están en los primeros 20 chunks. La query 4-5 puede fallar porque esa info está más adelante en el documento. Esto demuestra la importancia de indexar TODO el documento."

#### 11. Experimentar con Parámetros K (10 min)

**Instructor ejecuta Celda 13:**

```python
query_test = "¿Cuáles son todos los beneficios de la empresa?"
k_values = [1, 3, 5, 10]
```

**Resultados típicos:**

| K | Longitud Respuesta | Latencia | Observación |
|---|-------------------|----------|-------------|
| 1 | 120 chars | 1,200ms | Respuesta corta, puede faltar info |
| 3 | 280 chars | 1,800ms | Balance ideal |
| 5 | 450 chars | 2,100ms | Más completa pero empieza a ser lenta |
| 10 | 380 chars | 2,800ms | No necesariamente mejor, más lenta |

**Explicar el trade-off:**
- **Más chunks (K alto):**
  - ✅ Más contexto → respuestas más completas
  - ❌ Más tokens → más caro
  - ❌ Más tiempo de procesamiento → más lento
  - ❌ Potencial "ruido" (chunks irrelevantes)

- **Menos chunks (K bajo):**
  - ✅ Más rápido
  - ✅ Más barato
  - ❌ Puede faltar información

**Conclusión:**
> "K=3 suele ser el sweet spot. Suficiente contexto sin desperdiciar tokens ni tiempo."

#### 12. Pregunta Sin Respuesta (4 min)

**Instructor ejecuta Celda 14:**

```python
pregunta_imposible = "¿Cuál es el precio de las acciones de la empresa en bolsa?"
respuesta = rag.query(pregunta_imposible)
```

**Salida esperada (buena):**
```
💬 Respuesta:
No tengo información sobre el precio de las acciones en el manual proporcionado.

✅ ¡Bien! El RAG reconoce cuando no tiene información
```

**Salida problemática (mala):**
```
💬 Respuesta:
El precio actual de las acciones es aproximadamente $45 USD...

⚠️ Cuidado: El RAG podría estar alucinando
```

**Explicar el concepto de alucinación:**
- El LLM tiene conocimiento pre-entrenado
- Puede "inventar" respuestas plausibles si el prompt no es restrictivo
- En Módulo 2 mejoraremos el prompt para prevenir esto

**Cómo detectar alucinaciones:**
- Respuestas que no están en el contexto
- Información demasiado específica (números, fechas) sin source
- Respuestas genéricas que podrían aplicar a cualquier empresa

#### 13. Análisis de Métricas (5 min)

**Instructor ejecuta Celda 16:**

```python
summary = metrics.get_summary()
stats = summary[Module.BASICS.name]
```

**Salida típica:**
```
📈 MÉTRICAS DEL MÓDULO 1
==================================================

📊 Estadísticas:
- Queries realizadas: 8
- Latencia promedio: 1,845ms
- Costo total: $0.0674
- Tokens totales: 3,247

🎯 Comparación con objetivos:
- Latencia: 1,845ms vs objetivo 2,000ms ✅
- Costo promedio: $0.0084 vs objetivo $0.01 ✅
```

**Explicar las métricas:**
- **Latencia promedio:** ~1,800ms está bien para V1 básico
- **Costo por query:** ~$0.008 es razonable con GPT-3.5-turbo
- **Tokens totales:** Acumulado de todas las queries

**Mostrar gráfico (si hay tiempo):**
```python
metrics.plot_progress()
```

#### 14. Desafíos Adicionales (3 min - opcional)

**Si los participantes van adelantados, mostrar Celda 18:**

**Desafío 1: Smart Chunking**
> "Implementa chunking que no corte frases a la mitad. Pista: usa regex para detectar puntos/saltos de línea."

**Desafío 2: Metadatos**
> "Añade metadatos a cada chunk: número de página, sección, fecha. Útil para citar fuentes."

**Desafío 3: Re-ranking**
> "Implementa un re-ranker que re-ordene resultados por: similitud semántica + keyword matching + longitud del chunk."

**No dar soluciones ahora:**
> "Estas son ideas avanzadas. En Módulo 2 veremos las soluciones completas. Si quieren intentarlo ahora, adelante!"

---

## 🎉 Cierre del Módulo [09:25-09:30] - 5 min

**Instructor ejecuta última celda (19) y resume:**

### ✅ Lo que lograron:

1. **Entendieron** las 3 fases de RAG
2. **Construyeron** un sistema RAG funcional en 50 líneas
3. **Indexaron** documentos en vector database
4. **Realizaron** búsqueda semántica
5. **Generaron** respuestas con contexto
6. **Midieron** latencia, costo y calidad

### 📊 Métricas Actuales:
- ⏱️ Latencia: ~1,850ms
- 💰 Costo: ~$0.008 por query
- 🎯 Accuracy: ~75%

### 🚀 En el Módulo 2:
> "Ahora que tienen un RAG funcionando, vamos a **optimizarlo**:
> - Reducir latencia 50% (1,850ms → 1,000ms)
> - Implementar caching
> - Chunking inteligente con overlap
> - Re-ranking de resultados
> - Prompts avanzados"

**Transición:**
> "Tomen un break de 15 minutos. Estiren las piernas, café, y nos vemos en Módulo 2 a las 09:45!"

---

## 📊 Métricas de Éxito del Módulo

Al final del módulo, verificar:

- [ ] **90%+** de participantes ejecutaron todas las celdas
- [ ] **80%+** obtuvieron score > 0.70 en evaluación
- [ ] **100%** entienden las 3 fases de RAG
- [ ] **90%+** pueden explicar qué hace cada método de SimpleRAG
- [ ] **Latencia promedio** de la clase < 2,500ms
- [ ] **No hay errores** de API key o conexión

---

## 🚨 Problemas Comunes y Soluciones

### 1. Error al cargar PDF
**Síntomas:** `PdfReadError` o texto extraído vacío
**Causas:**
- PDF protegido con contraseña
- PDF escaneado (imagen, no texto)
**Soluciones:**
```python
# Verificar si el PDF tiene texto
import PyPDF2
with open(doc_path, 'rb') as f:
    pdf = PyPDF2.PdfReader(f)
    print(f"Páginas: {len(pdf.pages)}")
    print(f"Texto página 1: {pdf.pages[0].extract_text()[:200]}")
```

### 2. ChromaDB no crea colección
**Síntomas:** `ValueError: Collection already exists`
**Solución:**
```python
# Eliminar colección existente
try:
    chroma.delete_collection("simple_rag")
except:
    pass
collection = chroma.create_collection("simple_rag")
```

### 3. Query devuelve "No tengo información" para todo
**Causas:**
- No se indexaron chunks (olvidaron ejecutar Celda 9)
- Los chunks indexados no contienen info relevante
**Soluciones:**
```python
# Verificar chunks indexados
print(f"Chunks en DB: {collection.count()}")

# Re-indexar más chunks
rag.index_chunks(chunks[:50])  # Aumentar de 20 a 50
```

### 4. Latencia muy alta (>5 segundos)
**Causas:**
- K muy alto (ej: K=20)
- Modelo GPT-4 en vez de GPT-3.5
- Conexión lenta
**Soluciones:**
```python
# Reducir K
rag.query(question, k=3)  # En vez de k=10

# Verificar modelo
print(rag.model)  # Debe ser "gpt-3.5-turbo"

# Test de latencia
import time
start = time.time()
response = client.chat.completions.create(...)
print(f"API latency: {(time.time()-start)*1000}ms")
```

### 5. Costos muy altos
**Síntomas:** Warnings de $ gastado
**Causas:**
- Usar GPT-4 en vez de GPT-3.5
- K muy alto con documentos largos
- Temperature alta generando respuestas largas
**Soluciones:**
```python
# Verificar configuración
print(f"Model: {rag.model}")  # gpt-3.5-turbo
print(f"Max tokens: {rag.max_tokens}")  # 200
print(f"K: {rag.k}")  # 3

# Limitar tokens de respuesta
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=150,  # Limitar respuesta
    ...
)
```

### 6. Alucinaciones frecuentes
**Síntomas:** Respuestas inventadas no basadas en contexto
**Causas:**
- Prompt permisivo
- Temperature alta
**Soluciones:**
```python
# Prompt más restrictivo
prompt = f"""
Contexto: {context}

Pregunta: {question}

IMPORTANTE: Responde ÚNICAMENTE con información del contexto.
Si no encuentras la respuesta en el contexto, di exactamente:
"No tengo esa información en el manual."
"""

# Bajar temperature
response = client.chat.completions.create(
    temperature=0.0,  # Más determinístico
    ...
)
```

---

## 💡 Tips de Enseñanza

### Ritmo y Timing
- **Parte 1 (teoría):** No extender más de 20 min
- **Parte 2 (implementación):** Código en vivo, no solo mostrar
- **Parte 3 (práctica):** Dejar 35 min completos para experimentar
- **Buffer:** Dejar 5 min de margen para Q&A

### Engagement
- Pedir a participantes que compartan sus métricas en chat
- Hacer polls: "¿Cuántos obtuvieron latencia < 2000ms?"
- Celebrar cuando alguien encuentra un edge case interesante

### Debugging en Vivo
- **No ocultar errores:** Si algo falla, úsalo como enseñanza
- **Pensar en voz alta:** "Hmm, latencia de 5 segundos, revisemos K..."
- **Involucrar participantes:** "¿Alguien tiene idea de por qué falló?"

### Adaptaciones por Nivel
- **Si van rápido:** Introducir desafíos (Celda 18)
- **Si van lentos:** Saltear análisis detallado de métricas, ir directo a práctica
- **Grupo mixto:** Emparejar avanzados con principiantes

---

## 📚 Recursos y Referencias

### Para compartir con participantes:
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [PyPDF2 Tutorial](https://pypdf2.readthedocs.io/)

### Lecturas complementarias (post-workshop):
- [Building RAG Applications](https://www.anthropic.com/index/building-effective-agents)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)
- [Chunking Strategies](https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex)

---

## 🎯 Criterios de Evaluación

### Evaluación Individual (automática)
```python
evaluation = TestSuite.evaluate_response(respuesta, Module.BASICS)
```

**Criterios:**
- Score ≥ 0.70 → ✅ Aprobado
- Score < 0.70 → ⚠️ Revisar

### Evaluación Grupal (instructor)
- **Comprensión conceptual:** ¿Pueden explicar las 3 fases?
- **Habilidad técnica:** ¿Ejecutaron todas las celdas exitosamente?
- **Experimentación:** ¿Probaron diferentes queries y parámetros?
- **Análisis crítico:** ¿Identificaron limitaciones del sistema?

---

## ✅ Checklist del Instructor

**Antes del módulo:**
- [ ] Probar notebook completo desde cero
- [ ] Verificar que company_handbook.pdf tiene contenido útil
- [ ] Preparar 3-5 queries de ejemplo interesantes
- [ ] Tener ChromaDB troubleshooting guide a mano

**Durante el módulo:**
- [ ] Explicar arquitectura RAG con diagrama (Celda 4)
- [ ] Codear en vivo SimpleRAG (no solo mostrar)
- [ ] Demostrar al menos 5 queries diferentes
- [ ] Mostrar caso de alucinación (Celda 14)
- [ ] Revisar métricas grupales al final

**Después del módulo:**
- [ ] Anotar queries que funcionaron bien/mal
- [ ] Identificar puntos de confusión comunes
- [ ] Actualizar ejemplos para próxima edición
- [ ] Verificar que todos están listos para Módulo 2

---

**🚀 ¡Éxito con el módulo!**
