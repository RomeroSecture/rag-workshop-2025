# 🎓 Guía del Instructor - Notebook 03: Frameworks Profesionales
## Choose Your Path: LangChain vs LlamaIndex

---

## 📋 Información General

**Duración:** 120 minutos (12:30-15:30 con comida 14:00-15:00)
- **Teoría:** 45 min (12:30-13:15)
- **Práctica Parte 1:** 45 min (13:15-14:00)
- **Comida:** 60 min (14:00-15:00)
- **Práctica Parte 2:** 30 min (15:00-15:30)

**Objetivo:** Implementar RAG con frameworks profesionales y elegir el adecuado
**Nivel:** Avanzado
**Pre-requisitos:** Haber completado Módulos 1 y 2

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este módulo, los participantes serán capaces de:

1. ✅ **Comparar** LangChain vs LlamaIndex (pros/cons)
2. ✅ **Elegir** el framework adecuado según caso de uso
3. ✅ **Implementar** RAG con el framework elegido
4. ✅ **Añadir** memoria conversacional
5. ✅ **Integrar** agents y tools
6. ✅ **Alcanzar** 800ms de latencia (-20% vs Módulo 2)

---

## 📊 Métricas Target

| Métrica | Módulo 2 (Baseline) | Módulo 3 (Target) | Mejora |
|---------|---------------------|-------------------|---------|
| ⏱️ Latencia | 1000ms | 800ms | -20% |
| 💰 Costo | $0.008 | $0.006 | -25% |
| 🎯 Accuracy | 80% | 85% | +6% |
| 🔧 Mantenibilidad | Media | Alta | +++ |

---

## 🗓️ Timeline Detallado

| Tiempo | Sección | Actividad | Celdas |
|--------|---------|-----------|--------|
| 12:30-12:45 | Parte 1: Comparación | LangChain vs LlamaIndex demos | 1-5 |
| 12:45-13:00 | Parte 2: Decisión | Elegir path (A/B/C) | 6 |
| 13:00-13:45 | Parte 3: Implementación | Path elegido en profundidad | 7-11 |
| 13:45-14:00 | Parte 4: Features | Memory, Agents, Tools | 12-13 |
| **14:00-15:00** | **🍽️ COMIDA** | **Break largo** | - |
| 15:00-15:30 | Parte 5: Finalización | Benchmark y comparación | 14-16 |

---

## 📝 Guión de la Sesión

### PARTE 1: Comparación Side-by-Side [12:30-12:45] - 15 min

#### 1. Introducción a Frameworks (3 min)

**Instructor presenta:**

> "Hasta ahora hemos construido todo desde cero para entender los fundamentos. Ahora vamos a usar frameworks profesionales que abstraen mucha complejidad. Los dos principales son LangChain y LlamaIndex. Vamos a compararlos implementando el MISMO RAG con ambos."

**Conceptos clave:**
- **Framework = Biblioteca con componentes pre-construidos**
- **Abstracción = Menos código, más productividad**
- **Trade-off = Flexibilidad vs Simplicidad**

**Ejecutar Celda 1:**
```python
print("🔍 COMPARACIÓN: LangChain vs LlamaIndex")
```

**Salida esperada:**
```
✅ LangChain disponible
✅ LlamaIndex disponible
```

**Si faltan frameworks:**
```bash
pip install langchain langchain-openai
pip install llama-index
```

#### 2. Demo LangChain (5 min)

**Instructor ejecuta Celda 2:**

```python
def langchain_demo():
    """RAG con LangChain en 10 líneas"""
    # 1. Cargar documento
    loader = PyPDFLoader("../data/company_handbook.pdf")
    documents = loader.load()

    # 2. Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)

    # 3. Vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(texts, embeddings)

    # 4. Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=vectorstore.as_retriever()
    )

    # 5. Query
    result = qa_chain.run("¿Cuál es la política de vacaciones?")
    return result
```

**Explicar paso a paso:**
- **Loader:** Abstrae la lectura de PDFs
- **TextSplitter:** Chunking inteligente automático
- **Vectorstore:** Wrapper de ChromaDB con embeddings
- **Chain:** Pipeline completo de retrieval + QA
- **Query:** Una sola llamada para todo

**⏱️ Timing esperado:** ~2-3 segundos primera ejecución

#### 3. Demo LlamaIndex (5 min)

**Instructor ejecuta Celda 3:**

```python
def llamaindex_demo():
    """RAG con LlamaIndex en 5 líneas"""
    # 1. Cargar documentos
    documents = SimpleDirectoryReader('../data').load_data()

    # 2. Crear índice
    index = VectorStoreIndex.from_documents(documents)

    # 3. Query engine
    query_engine = index.as_query_engine(
        llm=LlamaOpenAI(temperature=0)
    )

    # 4. Query
    response = query_engine.query("¿Cuál es la política de vacaciones?")
    return str(response)
```

**Explicar diferencias clave:**
- **Menos líneas:** 5 vs 10
- **Más automático:** Índice se crea solo
- **Menos configuración:** Defaults inteligentes
- **Focus en búsqueda:** Optimizado para retrieval

**💡 Insight para compartir:**
> "LangChain da más control, LlamaIndex da más rapidez. Depende de tu necesidad."

#### 4. Tabla Comparativa (2 min)

**Instructor ejecuta Celda 5:**

Mostrar tabla de comparación:

| Aspecto | LangChain | LlamaIndex |
|---------|-----------|------------|
| **Filosofía** | Orquestación | Indexación |
| **Fortaleza** | Chains complejas, agents | Búsqueda avanzada |
| **Curva aprendizaje** | Media-Alta | Media |
| **Líneas de código** | +++ | + |
| **Flexibilidad** | Muy alta | Alta |
| **Ecosistema** | 250+ integr. | 100+ integr. |
| **Mejor para** | Pipelines complejos | Búsqueda optimizada |
| **Documentación** | Extensa | Muy buena |

**Explicar cada aspecto:**
- **Filosofía:** LangChain orquesta, LlamaIndex indexa
- **Fortaleza:** LangChain para apps complejas, LlamaIndex para búsqueda
- **Ecosistema:** Ambos tienen muchas integraciones

---

### PARTE 2: Elige Tu Camino [12:45-13:00] - 15 min

#### 5. Metodología "Choose Your Path" (5 min)

**Instructor presenta (Celda 6):**

> "Ahora viene la parte interesante. Cada uno va a elegir un camino:
> - **Path A: LangChain** - Si necesitas agents, chains complejas, orquestación
> - **Path B: LlamaIndex** - Si necesitas búsqueda avanzada, multi-índices
> - **Path C: Hybrid** - Si quieres combinar lo mejor de ambos
>
> No hay respuesta correcta. Depende de tu caso de uso."

**Guía para ayudar a elegir:**

**Elige LangChain si:**
- Necesitas agents con herramientas externas
- Quieres chains complejas multi-paso
- Requieres mucha personalización
- Tu app tiene workflows complejos
- Ejemplo: Chatbot que consulta APIs + base de datos + RAG

**Elige LlamaIndex si:**
- Enfocado principalmente en búsqueda
- Quieres prototipado rápido
- Necesitas query engines sofisticados
- Tu app es mayormente RAG puro
- Ejemplo: Sistema de búsqueda documental

**Elige Hybrid si:**
- Quieres lo mejor de ambos
- Sistema enterprise complejo
- Equipo grande con especialización
- Ejemplo: Plataforma con búsqueda (LlamaIndex) + automation (LangChain)

**Hacer poll:**
```
Por favor levanten la mano:
- Path A (LangChain): [contar]
- Path B (LlamaIndex): [contar]
- Path C (Hybrid): [contar]
```

**Anotar distribución para ajustar timing.**

#### 6. Preparación de Datos (5 min)

**IMPORTANTE:** Antes de elegir path, todos deben ejecutar celda de preparación:

```python
# Preparar chunks para todos los paths
from module_2_optimized import Module2_OptimizedRAG
rag_base = Module2_OptimizedRAG()
doc = rag_base.load_document()
chunks = rag_base.create_chunks(doc)
```

**Verificar que todos tienen chunks listos antes de continuar.**

#### 7. Dividir la Sala (5 min)

**Estrategia según distribución:**

**Si mayoría elige un path (>60%):**
- Enseñar ese path en detalle (30 min)
- Mostrar los otros paths brevemente (10 min cada uno)

**Si distribución equilibrada:**
- Enseñar Path A en detalle (20 min)
- Enseñar Path B en detalle (20 min)
- Mostrar Path C brevemente (5 min)

**Si hay grupos pequeños (<3 personas):**
- Sugerir unirse a un grupo más grande
- Ofrecer ayuda individual durante práctica

---

### PARTE 3: Implementación Profunda [13:00-13:45] - 45 min

#### PATH A: LangChain Completo (Si mayoría elige este)

**Instructor ejecuta Celda 8 paso a paso:**

##### 1. Clase Base (10 min)

```python
class Module3_LangChainRAG(Module2_OptimizedRAG):
    """RAG con LangChain - Extiende M2"""

    def __init__(self, initial_chunks=None):
        super().__init__()
        self.module = "M3_LangChain"

        if initial_chunks:
            self.chunks = initial_chunks

        self.setup_langchain()
        self.setup_agent()
```

**Explicar herencia:**
- Extendemos Module2_OptimizedRAG
- Mantenemos optimizaciones previas
- Añadimos funcionalidad LangChain

##### 2. Setup LangChain (10 min)

```python
def setup_langchain(self):
    # Embeddings
    self.embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # Vector Store
    self.vectorstore = Chroma(
        collection_name="m3_langchain",
        embedding_function=self.embeddings
    )

    # Añadir chunks de M2
    if self.chunks:
        texts = [chunk if isinstance(chunk, str) else
                chunk.get('text', str(chunk)) for chunk in self.chunks]
        self.vectorstore.add_texts(texts)

    # QA Chain
    self.qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0.3),
        chain_type="stuff",
        retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
```

**Conceptos a explicar:**
- **Embeddings:** Usamos modelo de OpenAI
- **Vectorstore:** ChromaDB con función de embeddings
- **RetrievalQA:** Chain pre-construida de LangChain
- **chain_type="stuff":** Mete todo el contexto en el prompt

##### 3. Agents y Tools (15 min) ⭐ **FEATURE CLAVE**

```python
def setup_agent(self):
    # Definir tools
    tools = [
        Tool(
            name="Company_QA",
            func=self.qa_chain.run,
            description="Útil para responder preguntas sobre políticas de la empresa"
        ),
        Tool(
            name="Calculator",
            func=lambda x: str(eval(x)),
            description="Útil para cálculos matemáticos"
        )
    ]

    # Inicializar agent
    self.agent = initialize_agent(
        tools,
        OpenAI(temperature=0),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=self.memory
    )
```

**Explicar Agents en detalle:**

**¿Qué es un Agent?**
- Sistema que decide qué herramienta usar
- Loop: Observar → Pensar → Actuar → Repetir
- Puede usar múltiples tools en secuencia

**Ejemplo de razonamiento del agent:**
```
Pregunta: "Si cada empleado tiene 22 días y somos 50, ¿cuántos días totales?"

Agent piensa:
1. Necesito saber cuántos días tiene cada empleado → Usar Company_QA
2. Tengo la respuesta: 22 días
3. Necesito multiplicar 22 * 50 → Usar Calculator
4. Respuesta final: 1,100 días
```

**Demo en vivo:**
```python
rag_langchain = Module3_LangChainRAG(initial_chunks=chunks)

queries = [
    "¿Cuántos días de vacaciones tienen los empleados?",
    "¿Y si tienen 5 años de antigüedad?",  # Usa memoria
    "Calcula cuántos días serían en 3 años"  # Usa calculadora
]

for q in queries:
    response = rag_langchain.query_with_memory(q)
    print(f"Q: {q}\nA: {response}\n")
```

**Salida esperada (con verbose=True):**
```
> Entering new AgentExecutor chain...
I need to find information about vacation policies
Action: Company_QA
Action Input: vacation days for employees
Observation: Employees get 22 days...
Thought: Now I know the answer
Final Answer: Los empleados tienen 22 días hábiles...
```

**Explicar cada parte del output:**
- **Thought:** El agent razona
- **Action:** Elige qué tool usar
- **Observation:** Resultado del tool
- **Final Answer:** Respuesta final

##### 4. Memoria Conversacional (10 min)

```python
self.memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
```

**Demo de memoria:**
```python
# Primera pregunta
"¿Cuántos días de vacaciones tienen?"
# Respuesta: 22 días

# Segunda pregunta (referencia a la primera)
"¿Y después de 5 años?"
# El agent recuerda el contexto y responde: 25 días
```

**Tipos de memoria en LangChain:**
- **ConversationBufferMemory:** Guarda todo
- **ConversationSummaryMemory:** Resume conversaciones largas
- **ConversationBufferWindowMemory:** Solo últimas N interacciones

#### PATH B: LlamaIndex Completo (Si mayoría elige este)

**Instructor ejecuta Celda 10 paso a paso:**

##### 1. Clase Base (5 min)

```python
class Module3_LlamaIndexRAG(Module2_OptimizedRAG):
    """RAG con LlamaIndex - Extiende M2"""

    def __init__(self, initial_chunks=None):
        super().__init__()
        if initial_chunks:
            self.chunks = initial_chunks
        self.setup_llamaindex()
```

##### 2. Setup LlamaIndex (10 min)

```python
def setup_llamaindex(self):
    # Convertir chunks a Documents
    documents = []
    for i, chunk in enumerate(self.chunks):
        text = chunk if isinstance(chunk, str) else chunk.get('text', str(chunk))
        doc = Document(
            text=text,
            metadata={"chunk_id": i, "source": "company_handbook"}
        )
        documents.append(doc)

    # Crear índice
    self.index = VectorStoreIndex.from_documents(
        documents,
        embed_model=OpenAIEmbedding(model="text-embedding-3-small")
    )

    # Query engine
    self.query_engine = self.index.as_query_engine(
        llm=LlamaOpenAI(model="gpt-3.5-turbo", temperature=0.3),
        similarity_top_k=3,
        streaming=False
    )
```

**Conceptos LlamaIndex:**
- **Document:** Objeto de LlamaIndex para texto + metadata
- **VectorStoreIndex:** Índice vectorial automático
- **QueryEngine:** Motor de búsqueda + generación

##### 3. Query con Contexto Mejorado (10 min)

```python
def query_with_context(self, question: str):
    response = self.query_engine.query(question)

    # Extraer fuentes
    sources = []
    if hasattr(response, 'source_nodes'):
        for node in response.source_nodes:
            sources.append({
                "text": node.text[:100],
                "score": getattr(node, 'score', 0.0)
            })

    return {
        "answer": str(response),
        "sources": sources
    }
```

**Ventaja de LlamaIndex:** Source tracking automático

##### 4. Features Avanzadas (20 min)

**Re-ranking con LlamaIndex:**
```python
from llama_index.indices.postprocessor import SentenceTransformerRerank

self.reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2",
    top_n=2
)

self.query_engine = self.index.as_query_engine(
    similarity_top_k=5,
    node_postprocessors=[self.reranker]
)
```

**Explicar re-ranking:**
- Primer paso: Embedding similarity (top 5)
- Segundo paso: Cross-encoder rerank (mejores 2)
- Resultado: Mayor precisión

**Demo:**
```python
rag_llamaindex = Module3_LlamaIndexRAG(initial_chunks=chunks)

result = rag_llamaindex.query_with_context("¿Cuál es la política de trabajo remoto?")
print(f"Respuesta: {result['answer']}")
print(f"Fuentes: {len(result['sources'])} documentos")
for i, source in enumerate(result['sources']):
    print(f"  {i+1}. Score: {source['score']:.3f} - {source['text'][:80]}...")
```

#### PATH C: Hybrid (Explicación breve - 10 min)

**Instructor ejecuta Celda 12:**

**Concepto:**
- LlamaIndex para indexación/búsqueda
- LangChain para orquestación/agents

```python
class Module3_HybridRAG:
    def setup_llamaindex_indexing(self):
        # LlamaIndex crea el índice
        self.llama_index = VectorStoreIndex.from_documents(documents)

    def setup_langchain_orchestration(self):
        # LangChain usa LlamaIndex como tool
        def search_with_llamaindex(query: str) -> str:
            return str(self.llama_index.as_query_engine().query(query))

        self.llama_tool = Tool(
            name="LlamaIndex_Search",
            func=search_with_llamaindex,
            description="Búsqueda optimizada"
        )
```

**Cuándo usar Hybrid:**
- Apps muy grandes
- Equipos especializados
- Lo mejor de ambos mundos
- Trade-off: Más complejidad

---

### PARTE 4: Features Avanzadas [13:45-14:00] - 15 min

#### 8. Comparación de Features (10 min)

**Ejecutar Celda 15:**

Comparar métricas de los 3 approaches:

| Framework | Latencia | Líneas código | Flexibilidad | Mejor para |
|-----------|----------|---------------|--------------|------------|
| LangChain | 850ms | 150 | Alta | Pipelines complejos |
| LlamaIndex | 750ms | 100 | Media | Búsqueda optimizada |
| Hybrid | 800ms | 200 | Muy Alta | Enterprise |

**Discusión guiada:**
> "¿Qué observan? LlamaIndex es más rápido porque está optimizado para búsqueda. LangChain da más control. Hybrid combina ambos pero añade complejidad."

#### 9. Decisión Final (5 min)

**Preguntas para el grupo:**
1. "¿Quién usaría LangChain en su proyecto? ¿Por qué?"
2. "¿Quién usaría LlamaIndex? ¿Por qué?"
3. "¿Alguien necesitaría Hybrid?"

**Casos de uso reales:**
- **LangChain:** Chatbot con acceso a 5 APIs diferentes
- **LlamaIndex:** Sistema de búsqueda en 1M documentos
- **Hybrid:** Plataforma con búsqueda + automatización

---

## 🍽️ COMIDA [14:00-15:00] - 60 min

**Instructor anuncia:**
> "¡Excelente trabajo esta mañana! Hora de recargar energías. Comida de 14:00 a 15:00. Volvemos puntuales a las 15:00 para terminar el Módulo 3 y comenzar producción."

**Durante la comida:**
- Estar disponible para preguntas
- Networking entre participantes
- Revisar notebooks de quienes van atrasados

---

### PARTE 5: Finalización y Benchmark [15:00-15:30] - 30 min

#### 10. Completar Implementaciones (15 min)

**Para quienes no terminaron:**
- Ayudar a completar su path elegido
- Asegurar que todos tienen algo funcionando

**Para quienes terminaron:**
- Experimentar con el otro path
- Comparar ambos approaches
- Optimizar parámetros

#### 11. Benchmark Final (10 min)

**Ejecutar queries de prueba con ambos frameworks:**

```python
test_queries = [
    "¿Política de vacaciones?",
    "¿Beneficios de empleados?",
    "¿Proceso de onboarding?"
]

# Comparar tiempos
for query in test_queries:
    # LangChain
    start = time.time()
    result_lc = rag_langchain.query(query)
    time_lc = (time.time() - start) * 1000

    # LlamaIndex
    start = time.time()
    result_li = rag_llamaindex.query(query)
    time_li = (time.time() - start) * 1000

    print(f"{query}: LC={time_lc:.0f}ms, LI={time_li:.0f}ms")
```

#### 12. Resumen y Conclusiones (5 min)

**Instructor ejecuta Celda 16:**

**Logros del módulo:**
1. ✅ Compararon frameworks profesionales
2. ✅ Eligieron según caso de uso
3. ✅ Implementaron con framework elegido
4. ✅ Añadieron memoria y agents
5. ✅ Alcanzaron ~800ms de latencia

**Métricas finales:**
- Latencia: 1000ms → 800ms (-20%)
- Código: -40% líneas vs custom
- Mantenibilidad: +++ (librerías con soporte)

**Transición a Módulo 4:**
> "Ahora tienen RAG con frameworks profesionales. Falta el último paso: llevarlo a producción. FastAPI, Docker, deployment. ¡Vamos!"

---

## 📊 Métricas de Éxito del Módulo

Al final del módulo, verificar:

- [ ] **90%+** eligieron un path y lo implementaron
- [ ] **80%+** entienden diferencias LangChain vs LlamaIndex
- [ ] **75%+** tienen agents/memory funcionando
- [ ] **Latencia promedio grupal** < 900ms
- [ ] **Accuracy promedio** > 0.83

---

## 🚨 Problemas Comunes y Soluciones

### 1. Frameworks no instalados
**Síntomas:** `ModuleNotFoundError`
**Solución:**
```bash
pip install langchain langchain-openai langchain-community
pip install llama-index llama-index-llms-openai llama-index-embeddings-openai
```

### 2. Agent no encuentra tools
**Síntomas:** Agent dice "I don't have access to that information"
**Causa:** Tool description no es clara
**Solución:**
```python
Tool(
    name="Company_QA",
    func=self.qa_chain.run,
    description="Use this tool to answer questions about company policies, benefits, vacation days, remote work, and HR topics. Input should be a question."
)
```

### 3. Memoria no funciona
**Síntomas:** Agent no recuerda conversaciones previas
**Causa:** Memory no está en el agent
**Solución:**
```python
self.agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=self.memory,  # ← IMPORTANTE
    verbose=True
)
```

### 4. LlamaIndex lento
**Síntomas:** Queries tardan >5 segundos
**Causa:** Indexando en cada query
**Solución:**
```python
# Crear índice UNA VEZ
if not hasattr(self, 'index'):
    self.index = VectorStoreIndex.from_documents(documents)

# Usar índice existente
query_engine = self.index.as_query_engine()
```

### 5. Chunks no se transfieren
**Síntomas:** "No tengo información" en queries
**Causa:** Chunks de M2 no llegaron al framework
**Solución:**
```python
# Verificar chunks
print(f"Chunks recibidos: {len(self.chunks) if hasattr(self, 'chunks') else 0}")

# Agregar a vectorstore
if self.chunks:
    texts = [str(chunk) for chunk in self.chunks]
    self.vectorstore.add_texts(texts)
```

---

## 💡 Tips de Enseñanza

### Gestión de Paths
- **Si >70% elige un path:** Enseñar ese en profundidad, otros brevemente
- **Si distribución 50/50:** Enseñar ambos paths principales
- **Si todos eligen diferente:** Enseñar LangChain (más didáctico)

### Timing de la Comida
- **CRÍTICO:** Empezar comida a las 14:00 exactas
- Avisar 5 min antes (13:55)
- Volver puntual a las 15:00

### Demos Efectivas
- **Agents:** Mostrar verbose=True para ver razonamiento
- **Memoria:** Hacer 3 queries seguidas para demostrar
- **Re-ranking:** Mostrar scores antes y después

### Engagement
- Poll en vivo de qué path eligen
- Compartir pantallas de participantes con implementaciones interesantes
- Crear competencia amistosa: "¿Quién logra latencia más baja?"

---

## 📚 Recursos Adicionales

### Para compartir con participantes:
- [LangChain Docs](https://python.langchain.com/)
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [LangChain vs LlamaIndex Comparison](https://blog.langchain.dev/langchain-vs-llamaindex/)
- [Agents Deep Dive](https://python.langchain.com/docs/modules/agents/)

### Lecturas avanzadas:
- [Building Production Agents](https://www.anthropic.com/research/building-effective-agents)
- [LlamaIndex Query Engines](https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/)
- [LangChain Expression Language](https://python.langchain.com/docs/expression_language/)

---

## ✅ Checklist del Instructor

**Antes del módulo:**
- [ ] Verificar que LangChain y LlamaIndex están instalados
- [ ] Probar ambos paths completos
- [ ] Preparar ejemplos de agents con verbose=True
- [ ] Tener backup de chunks preparados

**Durante el módulo:**
- [ ] Poll de qué path eligen
- [ ] Demo de agents con razonamiento visible
- [ ] Mostrar memoria conversacional en acción
- [ ] Comparar frameworks side-by-side
- [ ] Avisar comida 5 min antes

**Después del módulo:**
- [ ] Verificar que todos eligieron y completaron un path
- [ ] Recopilar feedback de frameworks
- [ ] Anotar qué path fue más popular
- [ ] Preparar para Módulo 4

---

**🚀 ¡Este es el módulo donde eligen su superpoder: LangChain o LlamaIndex!**
