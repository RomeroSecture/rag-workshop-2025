# 📅 Horario Oficial del RAG Workshop 2025

## ⏰ Duración Total
**10 horas:** 8:00 AM - 6:00 PM
- **9 horas efectivas** de contenido
- **1 hora** de comida

---

## 🌅 MAÑANA (8:00-14:00) - 6 horas

### 08:00-08:15 | Apertura y Setup (15 min)
**Notebook:** `00_inicio.ipynb`
- Bienvenida al workshop
- Verificación de ambiente (Codespaces, API keys)
- Demostración del problema vs solución

### 08:15-09:15 | Módulo 1 - Teoría (60 min)
**Notebook:** `01_fundamentos.ipynb` - Parte 1
- ¿Qué es RAG? Arquitectura completa
- Los 4 pilares: Documentos, Chunking, Embeddings, Vector DB
- Las 3 fases: Indexación, Retrieval, Generación
- Implementación de `SimpleRAG`

### 09:15-10:30 | Módulo 1 - Práctica (75 min)
**Notebook:** `01_fundamentos.ipynb` - Parte 2
- Cargar y procesar documentos
- Chunking e indexación
- Primera query guiada
- Experimentación con parámetros
- Análisis de métricas

### 10:30-10:45 | ☕ Break 1 (15 min)

### 10:45-11:30 | Módulo 2 - Teoría (45 min)
**Notebook:** `02_arquitectura.ipynb` - Parte 1
- Chunking con overlap
- Arquitectura de caching
- Re-ranking semántico
- Metadatos enriquecidos

### 11:30-12:15 | Módulo 2 - Práctica (45 min)
**Notebook:** `02_arquitectura.ipynb` - Parte 2
- Implementar cache
- Benchmark V1 vs V2
- Optimización de prompts
- Temperature tuning

### 12:15-12:30 | ☕ Break 2 (15 min)

### 12:30-13:15 | Módulo 3 - Teoría (45 min)
**Notebook:** `03_frameworks.ipynb` - Parte 1
- Comparación LangChain vs LlamaIndex
- Choose Your Path (A/B/C)
- Implementación con framework elegido

### 13:15-14:00 | Módulo 3 - Práctica Parte 1 (45 min)
**Notebook:** `03_frameworks.ipynb` - Parte 2
- Memory conversacional
- Agents y Tools
- Evaluación de calidad

---

## 🍽️ COMIDA (14:00-15:00) - 1 hora

---

## 🌆 TARDE (15:00-18:00) - 3 horas

### 15:00-15:30 | Módulo 3 - Práctica Parte 2 (30 min)
**Notebook:** `03_frameworks.ipynb` - Parte 3
- Completar implementación del framework elegido
- Comparación de métricas
- Decisión: ¿Qué framework usar en producción?

### 15:30-16:00 | Módulo 4 - Teoría (30 min)
**Notebook:** `04_produccion.ipynb` - Parte 1
- FastAPI para RAG
- Streaming de respuestas
- Autenticación y rate limiting
- Logging y monitoring

### 16:00-16:45 | Módulo 4 - Práctica (45 min)
**Notebook:** `04_produccion.ipynb` - Parte 2
- Implementar API completa
- Dockerización
- Deploy a Railway/Render
- Testing de endpoints

### 16:45-17:45 | 🏆 Proyecto Final (60 min)
**Notebook:** `05_proyecto_final.ipynb`
- Elegir caso de uso propio
- Implementación end-to-end
- Presentación al grupo (3 min cada uno)
- Feedback y mejoras

### 17:45-18:00 | 🎉 Cierre y Siguientes Pasos (15 min)
- Recap de lo aprendido
- Recursos para continuar
- Q&A abierto
- Certificados y feedback

---

## 📊 Distribución del Tiempo

| Módulo | Teoría | Práctica | Total |
|--------|--------|----------|-------|
| **M0 - Setup** | 15 min | - | 15 min |
| **M1 - Fundamentos** | 60 min | 75 min | 135 min |
| **M2 - Optimización** | 45 min | 45 min | 90 min |
| **M3 - Frameworks** | 45 min | 75 min | 120 min |
| **M4 - Producción** | 30 min | 45 min | 75 min |
| **M5 - Proyecto** | - | 60 min | 60 min |
| **Cierre** | 15 min | - | 15 min |
| **Breaks** | - | 30 min | 30 min |
| **Comida** | - | 60 min | 60 min |
| **TOTAL** | 210 min | 390 min | **600 min (10h)** |

**Contenido efectivo:** 540 min (9 horas)
**Descansos:** 60 min (1 hora)

---

## 🎯 Evolución de Métricas por Módulo

| Tiempo | Módulo | Latencia | Costo | Accuracy |
|--------|--------|----------|-------|----------|
| 08:15 | M1 inicio | - | - | - |
| 10:30 | M1 fin | 2000ms | $0.010 | 70% |
| 10:45 | M2 inicio | 2000ms | $0.010 | 70% |
| 12:15 | M2 fin | 1000ms | $0.008 | 80% |
| 12:30 | M3 inicio | 1000ms | $0.008 | 80% |
| 15:30 | M3 fin | 800ms | $0.006 | 85% |
| 15:30 | M4 inicio | 800ms | $0.006 | 85% |
| 16:45 | M4 fin | 500ms | $0.004 | 90% |

**Mejora total del día:**
- ⏱️ Latencia: 2000ms → 500ms (**-75%**)
- 💰 Costo: $0.010 → $0.004 (**-60%**)
- 🎯 Accuracy: 70% → 90% (**+29%**)

---

## ⏰ Puntos Clave de Timing

### Críticos - NO extender:
- **Comida:** 14:00-15:00 (exactamente 1 hora)
- **Cierre:** 17:45-18:00 (finalizar puntual)

### Flexibles - Pueden ajustarse:
- **Breaks:** Si van adelantados, pueden ser más cortos
- **Módulo 3 Práctica:** Dividido en 2 partes (pre/post comida) para dar flexibilidad

### Buffer recomendado:
- Dejar 5 min de margen al final de cada módulo
- Si van atrasados: Priorizar práctica sobre teoría
- Si van adelantados: Profundizar en desafíos avanzados

---

## 📝 Notas para el Instructor

### Gestión del tiempo:
1. **Usar cronómetro visible** para cada sección
2. **Avisar 5 min antes** de cada transición
3. **Ser estricto con breaks** (ni más ni menos)
4. **Comida puntual** - empezar 14:00, volver 15:00

### Si van atrasados:
- Módulo 1: Reducir experimentación con parámetros
- Módulo 2: Saltear ejercicios opcionales
- Módulo 3: Elegir solo 1 path (no mostrar todos)
- Módulo 4: Deploy opcional, solo mostrar código

### Si van adelantados:
- Módulo 1: Desafíos adicionales (smart chunking)
- Módulo 2: Ejercicios de optimización
- Módulo 3: Implementar múltiples paths
- Módulo 4: CI/CD completo

---

**Versión:** 1.0
**Última actualización:** Octubre 2025
**Total participantes recomendado:** 15-30 personas
