# 🎓 Guía del Instructor - Notebook 00: Inicio
## RAG Workshop 2025 - Sesión de Bienvenida y Setup

---

## 📋 Información General

**Duración:** 15 minutos (08:00-08:15)
**Objetivo:** Verificar que todos los participantes tengan el ambiente configurado correctamente
**Nivel:** Introductorio
**Pre-requisitos:** Ninguno (primera sesión)

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta sesión, los participantes deberán:

1. ✅ Tener GitHub Codespaces funcionando correctamente
2. ✅ Verificar instalación de todas las librerías (OpenAI, ChromaDB, LangChain, LlamaIndex)
3. ✅ Configurar correctamente su API Key de OpenAI
4. ✅ Ejecutar su primera llamada a la API exitosamente
5. ✅ Entender la estructura del proyecto y agenda del día
6. ✅ Conocer los archivos de datos disponibles

---

## 🗓️ Timeline Detallado

| Tiempo | Actividad | Descripción |
|--------|-----------|-------------|
| 00:00-00:02 | Apertura | Bienvenida y presentación del workshop |
| 00:02-00:05 | Setup | Abrir Codespaces y verificar carga |
| 00:05-00:08 | Verificación | Ejecutar celdas de verificación de ambiente |
| 00:08-00:12 | API Key | Configurar y validar API Key de OpenAI |
| 00:12-00:14 | Demostración | Mostrar el problema (LLM sin contexto) vs solución (RAG) |
| 00:14-00:15 | Cierre | Presentar estructura del proyecto y siguientes pasos |

---

## 📝 Guión de la Sesión

### 1. Apertura (2 min) [08:00-08:02]

**Instructor dice:**
> "¡Buenos días a todos! Bienvenidos al RAG Workshop 2025. Tenemos un día intenso por delante: 9 horas de contenido (8:00-18:00 con 1 hora de comida a las 14:00). Vamos a construir sistemas RAG de producción desde cero. Este notebook es para verificar que todo funciona correctamente antes de empezar."

**Acciones:**
- Compartir pantalla mostrando el README del repositorio
- Explicar brevemente la agenda del día (señalar la tabla en el notebook)
- Mencionar que TODO el desarrollo será en la nube (GitHub Codespaces)

### 2. Abrir GitHub Codespaces (3 min) [08:02-08:05]

**Instructor guía paso a paso:**

1. **Mostrar el badge de Codespaces en el README:**
   ```markdown
   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)]
   ```

2. **Clic en el badge:**
   - Esperar a que cargue el entorno (30-60 segundos)
   - Mostrar el terminal ejecutando `postCreateCommand.sh`

3. **Verificar que aparece el mensaje de bienvenida:**
   ```
   ╔═══════════════════════════════════════════════╗
   ║     🚀 RAG WORKSHOP 2025 - READY!            ║
   ╚═══════════════════════════════════════════════╝
   ```

**⚠️ Troubleshooting común:**
- Si Codespaces no inicia: Verificar que el usuario tiene permisos en GitHub
- Si falla postCreateCommand: Ejecutar manualmente: `bash .devcontainer/postCreateCommand.sh`
- Si no aparece Jupyter: Abrir manualmente el notebook desde el explorador de archivos

### 3. Verificación de Ambiente (3 min) [08:05-08:08]

**Instructor ejecuta Celda 2 en vivo:**

```python
# Verificar importaciones básicas
import sys, os
from pathlib import Path
sys.path.append(str(Path.cwd().parent / 'src'))
```

**Salida esperada:**
```
✅ Python 3.11.x
✅ OpenAI 1.45.0
✅ ChromaDB 0.5.0
✅ LangChain 0.2.11
✅ LlamaIndex 0.10.55
```

**Si aparecen errores:**

| Error | Solución |
|-------|----------|
| `❌ OpenAI no instalado` | `pip install openai==1.45.0` |
| `❌ ChromaDB no instalado` | `pip install chromadb==0.5.0` |
| Cualquier otro paquete faltante | `pip install -r requirements.txt` |

### 4. Configuración de API Key (4 min) [08:08-08:12]

**⚠️ CRÍTICO - Manejo de API Key:**

**Instructor debe:**

1. **NO mostrar su propia API Key en pantalla**
2. **Compartir API Key del workshop solo verbalmente o por chat privado**
3. **Explicar las dos opciones:**

**Opción 1: API Key Personal (RECOMENDADO para después del workshop)**
```bash
# Editar .env
OPENAI_API_KEY=sk-tu-clave-personal-aquí
```

**Opción 2: API Key del Workshop (SOLO para el taller)**
- El instructor comparte una API key temporal por chat privado
- Los participantes la copian en su archivo `.env`
- **Recordar:** Esta key se deshabilitará después del workshop

**Instructor ejecuta Celda 3:**
```python
# Verificar API Key
from dotenv import load_dotenv
import os
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
```

**Salida esperada:**
```
✅ API Key configurada correctamente
   Primeros caracteres: sk-proj...
```

**Si falla:**
- Verificar que el archivo `.env` está en la raíz del proyecto (no en `/notebooks/`)
- Verificar que la API key empieza con `sk-`
- Ejecutar `load_dotenv(override=True)` para forzar recarga

### 5. Test de Conexión con OpenAI (3 min) [08:12-08:14]

**Instructor ejecuta Celda 4:**

```python
from openai import OpenAI
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Di 'RAG Workshop Ready!' en 5 palabras"}],
    max_tokens=20
)
```

**Salida esperada:**
```
✅ Conexión con OpenAI exitosa!
⏱️  Latencia: 1200ms
🤖 Respuesta: ¡RAG Workshop está listo ya!
💰 Uso en esta query:
   - Tokens prompt: 18
   - Tokens respuesta: 8
   - Total: 26 tokens
   - Costo estimado: ~$0.000039
```

**⚠️ Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `AuthenticationError` | API key inválida | Re-generar key en platform.openai.com |
| `InsufficientQuotaError` | Sin créditos | Añadir $5 USD mínimo en billing |
| `RateLimitError` | Demasiadas peticiones | Esperar 1 minuto y reintentar |
| `ConnectionError` | Sin internet | Verificar conexión |

**💡 Tip del Instructor:**
> "Esta llamada costó menos de $0.0001. Durante el workshop gastaremos aproximadamente $0.50-$1.00 por persona. Si usan la API key compartida, no se preocupen por el costo."

### 6. Verificación de Archivos de Datos (Celda 3.5)

**Instructor ejecuta y explica:**

```python
# Verificar archivos de datos
from pathlib import Path
data_dir = Path("../data")
```

**Archivos esperados:**
- ✅ `company_handbook.pdf` (Manual del empleado - ejemplo principal)
- ✅ `technical_docs.pdf` (Documentación técnica)
- ✅ `faqs.json` (Preguntas frecuentes)
- ✅ `support_tickets.csv` (Tickets de soporte)

**Si faltan archivos:**
```bash
python src/utils.py --create-sample-data
```

### 7. Demostración del Problema y la Solución (2 min) [08:12-08:14]

**Instructor ejecuta Celdas 7 y 8:**

**Celda 7 - El Problema:**
```python
pregunta = "¿Cuántos días de vacaciones tienen los empleados en nuestra empresa?"
# Sin contexto - El modelo no sabe
```

**Salida:**
```
❌ Respuesta SIN RAG:
No tengo información específica sobre las políticas de tu empresa...
```

**Celda 8 - La Solución:**
```python
# Con RAG - Proporcionamos contexto del manual
contexto = """
Del Manual del Empleado (página 47):
- Empleados nuevos (0-5 años): 22 días hábiles
...
"""
```

**Salida:**
```
✅ Respuesta CON RAG:
Según el manual, los empleados nuevos tienen 22 días hábiles de vacaciones...
```

**Instructor enfatiza:**
> "¡Esto es exactamente lo que vamos a construir hoy! RAG permite que el LLM acceda a documentos específicos de tu empresa en tiempo real."

### 8. Visualización de Objetivos (Celda 10)

**Instructor muestra gráficos de evolución:**

- **Latencia:** 2000ms → 500ms (-75%)
- **Costo:** $0.010 → $0.004 (-60%)
- **Accuracy:** 70% → 90% (+20%)

**Explicación:**
> "Estos son nuestros objetivos para el día. En cada módulo mejoraremos estas métricas progresivamente. Al final tendrán un sistema listo para producción."

### 9. Estructura del Proyecto (Celda 12)

**Instructor explica la estructura:**

```
rag-workshop-2025/
├── 📓 notebooks/       # Vuestros notebooks de trabajo
│   ├── 00_inicio.ipynb      ← Estamos aquí
│   ├── 01_fundamentos.ipynb  ← Siguiente
│   └── ...
├── 📦 src/             # Código modular reutilizable
│   ├── module_1_basics.py
│   ├── module_2_optimized.py
│   └── ...
├── 📊 data/            # Documentos de prueba
│   └── company_handbook.pdf
└── 🔧 .env            # Configuración (API keys)
```

**Explicar filosofía:**
- **notebooks/** = Experimentación y aprendizaje
- **src/** = Código de producción reutilizable
- **data/** = Datos de ejemplo (no reales de producción)

### 10. Cierre y Transición (1 min) [08:14-08:15]

**Instructor resume:**

✅ **Checklist completado:**
- [x] Codespaces funcionando
- [x] Librerías instaladas
- [x] API Key configurada
- [x] Primera llamada exitosa
- [x] Datos verificados
- [x] Estructura clara

**Instructor dice:**
> "¡Perfecto! Todos tienen el ambiente listo. Ahora vamos directamente al Módulo 1 donde construirán su primer sistema RAG funcional en 30 minutos. Abran el notebook `01_fundamentos.ipynb`"

---

## 📊 Métricas de Éxito

Al final de esta sesión, verificar:

- [ ] **100% de participantes** tienen Codespaces corriendo
- [ ] **100%** ejecutaron la celda de verificación exitosamente
- [ ] **90%+** tienen API Key configurada (algunos pueden necesitar ayuda extra)
- [ ] **90%+** obtuvieron respuesta de OpenAI exitosamente
- [ ] **Todos** entienden la estructura del proyecto

---

## 🚨 Problemas Comunes y Soluciones

### 1. Codespaces no inicia
**Síntomas:** Pantalla en blanco o error de permisos
**Soluciones:**
- Verificar que el usuario está autenticado en GitHub
- Probar desde navegador en incógnito
- Crear Codespace manualmente desde la pestaña "Code" del repo

### 2. API Key no se reconoce
**Síntomas:** `❌ API Key no configurada`
**Soluciones:**
- Verificar ubicación del archivo `.env` (debe estar en raíz, no en `/notebooks/`)
- Ejecutar `load_dotenv(override=True)` para forzar recarga
- Verificar que no hay espacios extra: `OPENAI_API_KEY=sk-xxx` (sin espacios)

### 3. Error de cuota/créditos
**Síntomas:** `InsufficientQuotaError`
**Soluciones:**
- Si usan API key compartida: notificar al instructor (puede estar agotada)
- Si usan API key personal: añadir créditos en https://platform.openai.com/account/billing
- Cambiar a la API key del workshop si estaban usando personal

### 4. Paquetes no instalados
**Síntomas:** `ModuleNotFoundError: No module named 'xxx'`
**Soluciones:**
```bash
# Reinstalar todo
pip install -r requirements.txt

# O individualmente
pip install openai chromadb langchain llama-index
```

### 5. Archivos de datos faltantes
**Síntomas:** `❌ company_handbook.pdf FALTANTE`
**Soluciones:**
```bash
# Generar datos de ejemplo
python src/utils.py --create-sample-data

# O descargar del repo principal
git pull origin main
```

---

## 💡 Tips de Enseñanza

### Ritmo
- ⏰ **IMPORTANTE:** Este módulo debe durar exactamente 15 minutos
- Si algunos participantes están atrasados, ayudarlos durante el break
- No extender más de 20 minutos para no atrasar el resto del día

### Engagement
- Pedir a los participantes que escriban en el chat cuando completen cada celda
- Crear un canal de Slack/Discord para troubleshooting en vivo
- Tener un asistente monitoreando el chat mientras enseñas

### Prevención de problemas
- **Enviar instrucciones 24h antes:** Email con link al repo y pasos previos
- **Tener API keys de respaldo:** Mínimo 2-3 keys con $20 cada una
- **Grabar la sesión:** Para quienes tengan problemas técnicos

### Adaptaciones
- **Si todos van rápido (12 min):** Mostrar también las gráficas de métricas (Celda 10)
- **Si van lentos (>18 min):** Saltear las celdas de demostración y ir directo a Módulo 1

---

## 📚 Recursos Adicionales

### Para compartir con participantes:
- [Documentación OpenAI](https://platform.openai.com/docs)
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [Jupyter Shortcuts](https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330)

### Para el instructor:
- `SECURITY_API_KEYS.md` - Mejores prácticas de manejo de API keys
- `DEPLOYMENT_SUCCESS.md` - Información de deployment del workshop
- `scripts/verify_setup.py` - Script automático de verificación

---

## 🎯 Criterios de Evaluación

| Criterio | Peso | Cómo verificar |
|----------|------|----------------|
| Codespaces activo | 30% | Ver pantallas compartidas |
| API key funcionando | 40% | Verificar salida de Celda 4 |
| Librerías instaladas | 20% | Verificar salida de Celda 2 |
| Datos disponibles | 10% | Verificar Celda 3.5 |

**Threshold de éxito:** 90% de participantes con score ≥80%

---

## ✅ Checklist del Instructor

**Antes del workshop:**
- [ ] Probar el Codespace desde cero (cuenta nueva)
- [ ] Verificar que API keys compartidas tienen créditos ($20+ cada una)
- [ ] Tener números de contacto de 2-3 participantes para comunicación
- [ ] Preparar slides con agenda y objetivos

**Durante la sesión:**
- [ ] Compartir pantalla con notebook 00_inicio.ipynb abierto
- [ ] Tener ventana del chat visible para preguntas
- [ ] Cronometrar cada sección
- [ ] Tomar nota de problemas comunes para siguientes ediciones

**Después de la sesión:**
- [ ] Verificar con cada participante que están listos
- [ ] Anotar tiempo real vs planeado
- [ ] Identificar cuellos de botella para futuros workshops

---

## 🔗 Enlaces Rápidos

- **Repo:** https://github.com/RomeroSecture/rag-workshop-2025
- **Codespaces:** https://github.com/codespaces
- **API Keys:** https://platform.openai.com/api-keys
- **Billing:** https://platform.openai.com/account/billing
- **Slack/Discord:** [Añadir link del canal del workshop]

---

**¡Éxito con el workshop!** 🚀
