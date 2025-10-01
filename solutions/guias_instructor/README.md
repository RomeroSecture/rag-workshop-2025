# 🎓 Guías del Instructor - RAG Workshop 2025

## 📚 Guías Disponibles

Esta carpeta contiene las guías completas del instructor para cada notebook del workshop. Cada guía incluye:

- ⏱️ **Timeline detallado** con tiempos específicos
- 📝 **Guión de la sesión** con qué decir y cuándo
- 🎯 **Objetivos de aprendizaje** claros y medibles
- 🚨 **Troubleshooting** de problemas comunes
- 💡 **Tips de enseñanza** y mejores prácticas
- 📊 **Métricas de éxito** para evaluar el módulo
- ✅ **Checklist** pre/durante/post sesión

---

## 📖 Índice de Guías

### [Notebook 00: Inicio](NOTEBOOK_00_inicio_guia.md)
**Duración:** 15 minutos (08:00-08:15)

**Objetivos:**
- ✅ Verificar ambiente (Codespaces, librerías, API key)
- ✅ Primera llamada exitosa a OpenAI
- ✅ Entender estructura del proyecto
- ✅ Visualizar objetivos del día

**Temas clave:**
- Setup de GitHub Codespaces
- Configuración de API Key (seguridad)
- Verificación de datos de ejemplo
- Demostración del problema (LLM sin contexto) vs solución (RAG)

---

### [Notebook 01: Fundamentos](NOTEBOOK_01_fundamentos_guia.md)
**Duración:** 75 minutos (08:15-09:30)

**Objetivos:**
- ✅ Construir sistema RAG completo en 50 líneas
- ✅ Implementar las 3 fases: Indexación, Retrieval, Generación
- ✅ Realizar búsqueda semántica
- ✅ Medir latencia, costo y calidad

**Temas clave:**
- Arquitectura RAG (diagrama detallado)
- Clase `SimpleRAG` método por método
- Chunking básico (sin overlap)
- ChromaDB y embeddings automáticos
- Primera query guiada
- Experimentación con parámetro K

**Métricas target:**
- Latencia: ~2000ms
- Costo: ~$0.01/query
- Accuracy: ~70%

---

### [Notebook 02: Arquitectura y Optimización](NOTEBOOK_02_arquitectura_guia.md)
**Duración:** 90 minutos (09:45-11:15)

**Objetivos:**
- ✅ Implementar chunking con overlap (+25% cobertura)
- ✅ Aplicar caching (speedup 12x)
- ✅ Implementar re-ranking semántico
- ✅ Optimizar prompts y temperature
- ✅ Reducir latencia 50% (2000ms → 1000ms)

**Temas clave:**
- Chunking inteligente con overlap de 200 chars
- Cache para queries repetidas
- Re-ranking multi-señal (semantic + keyword + position + length + metadata)
- Prompt engineering (básico vs optimizado)
- Temperature tuning (0.0 vs 0.3 vs 0.7 vs 1.0)
- Metadatos enriquecidos

**Mejoras logradas:**
- Latencia: -45% (2000ms → 1100ms)
- Costo: -20% ($0.010 → $0.008)
- Accuracy: +20% (0.70 → 0.84)

**Ejercicios prácticos:**
1. Encontrar chunk_size óptimo
2. Implementar filtrado por metadatos
3. Crear prompt técnico especializado

---

### [Notebook 03: Frameworks Avanzados](NOTEBOOK_03_frameworks_guia.md)
**Duración:** 90 minutos (12:00-13:30)

**Objetivos:**
- ✅ Implementar RAG con LangChain
- ✅ Implementar RAG con LlamaIndex
- ✅ Comparar frameworks (pros/cons)
- ✅ Usar agents y tools
- ✅ Evaluar calidad objetivamente

**Temas clave:**
- LangChain: Chains, Retrievers, Agents
- LlamaIndex: Query Engine, Service Context, Response Synthesis
- Comparación framework-by-framework
- Evaluación con LangSmith/LlamaIndex Eval
- Cuándo usar qué framework

**Decisión de frameworks:**
- **LangChain:** Mejor para aplicaciones complejas, agents, multi-step
- **LlamaIndex:** Mejor para indexación avanzada, query engines, rapid prototyping

---

### [Notebook 04: Producción](NOTEBOOK_04_produccion_guia.md)
**Duración:** 75 minutos (13:45-15:00)

**Objetivos:**
- ✅ Crear API FastAPI completa
- ✅ Implementar streaming de respuestas
- ✅ Añadir autenticación y rate limiting
- ✅ Configurar logging y monitoring
- ✅ Deploy a cloud (Railway/Render)

**Temas clave:**
- FastAPI endpoints (index, query, health)
- Streaming con Server-Sent Events
- Autenticación Bearer token
- Rate limiting por usuario
- Logging estructurado (Loguru)
- Monitoring con métricas Prometheus
- Docker containerization
- CI/CD con GitHub Actions

**12 TODOs de producción:**
1. Endpoint de indexación
2. Endpoint de query
3. Streaming de respuestas
4. Autenticación
5. Rate limiting
6. Logging
7. Métricas
8. Health checks
9. Dockerfile
10. Docker Compose
11. CI/CD pipeline
12. Deploy a cloud

---

### [Notebook 05: Proyecto Final](NOTEBOOK_05_proyecto_final_guia.md)
**Duración:** 45 minutos (15:00-15:45)

**Objetivos:**
- ✅ Aplicar todo lo aprendido a un caso real
- ✅ Construir RAG completo end-to-end
- ✅ Presentar solución al grupo
- ✅ Recibir feedback

**Temas clave:**
- Elección de caso de uso propio
- Arquitectura end-to-end
- Implementación guiada con TODOs
- Presentación de 3 minutos
- Evaluación con rubric

**3 Niveles de implementación:**

**Nivel 1 - Básico (30 min):**
- RAG simple con LangChain o LlamaIndex
- 1 documento de ejemplo
- Query básica
- Sin optimizaciones

**Nivel 2 - Intermedio (45 min):**
- RAG optimizado con cache y re-ranking
- Múltiples documentos
- API FastAPI básica
- Evaluación de calidad

**Nivel 3 - Avanzado (60 min):**
- RAG con agents y tools
- Indexación de múltiples fuentes
- API completa con auth y streaming
- Deploy a cloud
- Monitoring y observability

---

## 📊 Resumen de Métricas por Módulo

| Módulo | Latencia | Costo | Accuracy | Duración |
|--------|----------|-------|----------|----------|
| 0 - Inicio | - | - | - | 15 min |
| 1 - Fundamentos | 2000ms | $0.010 | 70% | 75 min |
| 2 - Optimización | 1000ms | $0.008 | 80% | 90 min |
| 3 - Frameworks | 800ms | $0.006 | 85% | 90 min |
| 4 - Producción | 500ms | $0.004 | 90% | 75 min |
| 5 - Proyecto Final | Varía | Varía | Varía | 45 min |

**Evolución total del día:**
- ⏱️ Latencia: 2000ms → 500ms (**-75%**)
- 💰 Costo: $0.010 → $0.004 (**-60%**)
- 🎯 Accuracy: 70% → 90% (**+29%**)

---

## 🎯 Estrategia Pedagógica Global

### Filosofía del Workshop

**Aprendizaje progresivo:**
1. **Módulo 1:** Construir desde cero para entender fundamentos
2. **Módulo 2:** Optimizar paso a paso con técnicas avanzadas
3. **Módulo 3:** Usar frameworks profesionales (abstracción)
4. **Módulo 4:** Llevar a producción con mejores prácticas
5. **Módulo 5:** Aplicar a caso real del participante

**Niveles de dificultad:**
- 🟢 **Nivel 1 (Módulos 0-1):** Typing along - Copiar código, entender conceptos
- 🟡 **Nivel 2 (Módulo 2):** Fill in the blanks - Completar TODOs guiados
- 🟠 **Nivel 3 (Módulos 3-4):** Choose your path - Elegir tecnologías
- 🔴 **Nivel 4 (Módulo 5):** Build from scratch - Proyecto propio

### Gestión del Tiempo

**Timeline general del día:**
```
08:00-08:15  Inicio (15 min)           ☕ Setup
08:15-09:30  Módulo 1 (75 min)         🏗️ Fundamentos
09:30-09:45  Break (15 min)            🚶 Networking
09:45-11:15  Módulo 2 (90 min)         ⚡ Optimización
11:15-12:00  Almuerzo (45 min)         🍕 Recargar
12:00-13:30  Módulo 3 (90 min)         🔧 Frameworks
13:30-13:45  Break (15 min)            ☕ Stretch
13:45-15:00  Módulo 4 (75 min)         🚀 Producción
15:00-15:45  Módulo 5 (45 min)         💡 Proyecto
15:45-16:00  Cierre (15 min)           🎉 Q&A
```

**Total:** 8 horas (480 min)
- Enseñanza activa: 390 min (81%)
- Breaks: 75 min (16%)
- Cierre: 15 min (3%)

### Engagement Strategies

**Cada módulo incluye:**
- 📊 **Métricas visibles:** Dashboards y gráficos de progreso
- 🏆 **Gamificación:** Celebrar mejoras ("¡45% más rápido!")
- 💬 **Participación:** Polls, preguntas en chat, shares de pantalla
- 🧪 **Experimentos:** Probar parámetros, ver qué pasa
- 🚨 **Troubleshooting en vivo:** Usar errores como enseñanza

**Adaptaciones por audiencia:**
- **Desarrolladores senior:** Enfatizar arquitectura, trade-offs, producción
- **Data scientists:** Enfatizar evaluación, métricas, experimentación
- **Audiencia mixta:** Emparejar niveles, ejercicios diferenciados

---

## 🚨 Troubleshooting Transversal

### Problemas Comunes a Todos los Módulos

#### 1. API Key Issues
**Síntomas:** `AuthenticationError`, `InvalidRequestError`
**Soluciones:**
- Verificar formato: debe empezar con `sk-`
- Verificar archivo `.env` en raíz del proyecto
- Ejecutar `load_dotenv(override=True)`
- Generar nueva key en platform.openai.com

#### 2. Quota/Billing Issues
**Síntomas:** `InsufficientQuotaError`, `RateLimitError`
**Soluciones:**
- Añadir créditos ($5 mínimo) en platform.openai.com/account/billing
- Usar API key compartida del workshop
- Reducir frecuencia de queries (añadir `time.sleep(1)`)
- Usar modelo más barato (gpt-3.5-turbo vs gpt-4)

#### 3. Latencia Extrema (>10 segundos)
**Causas:**
- K muy alto (>20)
- Modelo GPT-4 en vez de GPT-3.5
- Max tokens muy alto (>2000)
- Conexión lenta

**Debug:**
```python
import time

# Test de latencia por componente
start = time.time()
results = collection.query(...)  # Retrieval
retrieval_time = (time.time() - start) * 1000

start = time.time()
response = client.chat.completions.create(...)  # Generation
generation_time = (time.time() - start) * 1000

print(f"Retrieval: {retrieval_time}ms")
print(f"Generation: {generation_time}ms")
```

#### 4. Respuestas de Baja Calidad
**Causas:**
- Chunks muy pequeños (contexto insuficiente)
- K muy bajo (información incompleta)
- Prompt permisivo (alucinaciones)
- Temperature muy alta (respuestas divagantes)

**Checklist de diagnóstico:**
```python
# 1. Verificar chunks
print(f"Chunk size: {len(chunks[0])}")
print(f"Overlap: {overlap}")

# 2. Verificar retrieval
print(f"K: {k}")
print(f"Retrieved chunks preview: {results['documents'][0][:200]}")

# 3. Verificar prompt
print(f"Prompt length: {len(prompt.split())} words")
print(f"Temperature: {temperature}")

# 4. Verificar respuesta
print(f"Response length: {len(response)}")
print(f"Contains 'no sé' or 'no tengo': {'no sé' in response.lower()}")
```

---

## 💡 Tips Generales de Enseñanza

### Antes del Workshop

**1 semana antes:**
- [ ] Enviar email con link al repo y badge de Codespaces
- [ ] Pedir a participantes que creen cuenta OpenAI
- [ ] Compartir agenda detallada y objetivos

**1 día antes:**
- [ ] Probar TODO el workshop en Codespace limpio
- [ ] Verificar API keys compartidas tienen crédito ($20+ cada una)
- [ ] Preparar slides de introducción
- [ ] Crear canal Slack/Discord para soporte

**Mañana del workshop:**
- [ ] Llegar 30 min antes para setup técnico
- [ ] Probar screen sharing y audio
- [ ] Tener backup de API keys
- [ ] Preparar café ☕

### Durante el Workshop

**Gestión de preguntas:**
- Preguntas rápidas (<1 min): Responder en vivo
- Preguntas complejas (>2 min): "Gran pregunta, la retomamos en el break"
- Preguntas fuera de scope: "Excelente tema, fuera del workshop pero te comparto recursos después"

**Manejo de timing:**
- Usar temporizador visible para cada sección
- Si van atrasados: Saltear ejercicios opcionales, compartir soluciones
- Si van adelantados: Profundizar en desafíos avanzados

**Engagement continuo:**
- Cada 20 min: Poll rápido o pregunta al grupo
- Cada módulo: Celebrar logros ("¡Miren sus métricas!")
- Usar nombres: "Como mencionó María...", "La pregunta de Juan..."

### Después del Workshop

**Inmediatamente después:**
- [ ] Compartir slides y soluciones completas
- [ ] Enviar encuesta de feedback (Google Forms)
- [ ] Crear lista de recursos adicionales

**Semana siguiente:**
- [ ] Analizar feedback y métricas
- [ ] Responder preguntas post-workshop por email/Slack
- [ ] Actualizar guías con lessons learned
- [ ] Compartir proyectos destacados de participantes

---

## 📚 Recursos del Instructor

### Documentación Técnica
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [LangChain Python Docs](https://python.langchain.com/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Troubleshooting Guides
- [SECURITY_API_KEYS.md](../../SECURITY_API_KEYS.md) - Manejo seguro de API keys
- [DEPLOYMENT_SUCCESS.md](../../DEPLOYMENT_SUCCESS.md) - Info de deployment
- [scripts/verify_setup.py](../../scripts/verify_setup.py) - Script de verificación automática

### Soluciones Completas
- [solutions/nivel_2_workshop/](../) - Código de todos los ejercicios
- [solutions/README_SOLUCIONES.md](../README_SOLUCIONES.md) - Documentación de soluciones

### Material Complementario
- [Building Production RAG](https://www.anthropic.com/index/building-effective-agents)
- [RAG Best Practices](https://eugeneyan.com/writing/llm-patterns/)
- [Vector Database Comparison](https://www.pinecone.io/learn/vector-database/)
- [LLM Evaluation Methods](https://humanloop.com/blog/evaluating-llm-apps)

---

## ✅ Checklist Master del Instructor

### Pre-Workshop (1 semana antes)
- [ ] Probar workshop completo en Codespace limpio
- [ ] Verificar 3+ API keys con $20+ crédito cada una
- [ ] Enviar email a participantes con:
  - [ ] Link al repo y badge de Codespaces
  - [ ] Instrucciones para crear cuenta OpenAI
  - [ ] Agenda detallada del día
  - [ ] Pre-requisitos (ninguno, pero sugerencias de preparación)
- [ ] Crear canal de comunicación (Slack/Discord)
- [ ] Preparar slides de introducción
- [ ] Revisar todas las guías del instructor

### Pre-Workshop (día anterior)
- [ ] Re-verificar API keys tienen crédito
- [ ] Hacer commit final de últimos cambios
- [ ] Preparar computadora (cerrar apps innecesarias)
- [ ] Probar screen sharing y audio
- [ ] Imprimir agenda como backup

### Durante el Workshop
- [ ] Llegar 30 min antes
- [ ] Test técnico: audio, video, screen sharing
- [ ] Tener backup de API keys a mano
- [ ] Cronometrar cada módulo
- [ ] Tomar notas de:
  - [ ] Preguntas frecuentes
  - [ ] Puntos de confusión
  - [ ] Timing real vs planeado
  - [ ] Errores inesperados

### Post-Workshop
- [ ] Compartir soluciones y recursos
- [ ] Enviar encuesta de feedback
- [ ] Responder preguntas pendientes
- [ ] Actualizar guías con lessons learned
- [ ] Analizar métricas y feedback
- [ ] Planear mejoras para próxima edición

---

## 🎯 Métricas de Éxito del Workshop Completo

### Indicadores Cuantitativos
- [ ] **Completación:** >90% terminan los 5 módulos
- [ ] **Técnico:** >85% logran deploy exitoso (Módulo 4)
- [ ] **Performance:** Promedio grupal de latencia <600ms (Módulo 4)
- [ ] **Quality:** Promedio grupal de accuracy >85% (Módulo 4)
- [ ] **Engagement:** >80% completan proyecto final (Módulo 5)

### Indicadores Cualitativos
- [ ] Participantes pueden explicar arquitectura RAG
- [ ] Participantes identifican cuándo usar LangChain vs LlamaIndex
- [ ] Participantes conocen best practices de producción
- [ ] Participantes tienen proyecto funcional propio
- [ ] NPS (Net Promoter Score) >8/10

### Feedback a Recolectar
1. **Contenido:** ¿Fue relevante y bien estructurado?
2. **Ritmo:** ¿Muy rápido/lento/adecuado?
3. **Hands-on:** ¿Suficiente práctica?
4. **Instructor:** ¿Explicaciones claras?
5. **Aplicabilidad:** ¿Pueden usar esto en su trabajo?
6. **Recomendación:** ¿Lo recomendarían? (NPS)

---

## 📞 Contacto y Soporte

**Durante el workshop:**
- Canal Slack/Discord del workshop
- Chat de la videoconferencia
- Levantar la mano en Zoom

**Post-workshop:**
- Email: aromero@secture.com
- GitHub Issues: https://github.com/RomeroSecture/rag-workshop-2025/issues
- Slack/Discord (mantener abierto 1 semana post-workshop)

---

## 🎉 ¡Éxito con el Workshop!

Estas guías han sido diseñadas para garantizar una experiencia de aprendizaje excepcional. Recuerda:

✨ **La clave es el balance:** Teoría suficiente para entender, práctica abundante para consolidar.

🎯 **Adaptabilidad:** Usa estas guías como base, ajusta según tu audiencia.

❤️ **Pasión:** Tu entusiasmo es contagioso. Si tú crees en RAG, ellos también creerán.

🚀 **Impacto:** Al final del día, 30+ personas sabrán construir sistemas RAG de producción. ¡Eso es tremendo!

---

**¡Vamos a crear una generación de RAG builders!** 🎓
