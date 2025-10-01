# 👨‍🏫 Checklist del Instructor - Día del Workshop

**Workshop**: RAG 2025 - De Cero a Producción
**Duración**: 8 horas
**Formato**: GitHub Codespaces (100% en la nube)

---

## 📅 1 SEMANA ANTES DEL WORKSHOP

### ✅ Preparación del Repositorio

- [ ] **Push a GitHub**
  ```bash
  cd /Users/antonioromero/Desktop/Proyectos/rag-workshop-2025
  git add .
  git commit -m "Workshop ready for participants"
  git push origin main
  ```

- [ ] **Verificar GitHub Codespaces está habilitado**
  - Settings → Codespaces → Allow for this repository
  - Verificar que `.devcontainer/devcontainer.json` existe

- [ ] **Hacer el repo público o invitar participantes**
  - Opción A: Hacerlo público
  - Opción B: Añadir colaboradores en Settings → Collaborators

- [ ] **Crear badge de "Open in Codespaces"** en README
  ```markdown
  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/[TU-USUARIO]/rag-workshop-2025?quickstart=1)
  ```

### ✅ Testing Completo

- [ ] **Crear un Codespace de prueba tú mismo**
  1. Ir al repo en GitHub
  2. Code → Codespaces → Create codespace
  3. Esperar instalación (2-3 min)
  4. Verificar que todo funciona

- [ ] **Ejecutar script de verificación**
  ```bash
  python scripts/verify_setup.py
  ```
  - Debe pasar TODAS las verificaciones

- [ ] **Probar todos los notebooks en orden**
  - [ ] 00_inicio.ipynb
  - [ ] 01_fundamentos.ipynb
  - [ ] 02_arquitectura.ipynb
  - [ ] 03_frameworks.ipynb
  - [ ] 04_produccion.ipynb
  - [ ] 05_proyecto_final.ipynb

- [ ] **Verificar que soluciones NO están en main**
  ```bash
  # La rama main NO debe tener carpeta solutions/
  ls solutions/  # Debe fallar o estar vacía
  ```

- [ ] **Asegurar que rama solutions está separada**
  ```bash
  git checkout solutions
  ls solutions/  # Debe tener todas las soluciones
  git checkout main
  ```

---

## 📧 3 DÍAS ANTES - Email a Participantes

### Enviar Instrucciones Pre-Workshop

**Asunto**: RAG Workshop 2025 - Instrucciones de Acceso (TODO EN LA NUBE ☁️)

```markdown
Hola [Nombre],

¡El workshop está a 3 días! 🎉

**IMPORTANTE: NO necesitas instalar nada en tu computadora**
Todo funciona 100% en la nube con GitHub Codespaces.

### 📋 LO ÚNICO QUE NECESITAS:

1. **Cuenta de GitHub** (gratuita)
   - Si no tienes: https://github.com/signup
   - 60 horas/mes de Codespaces gratis incluidas

2. **API Key de OpenAI** ($5 USD de créditos recomendados)
   - Crear cuenta: https://platform.openai.com/signup
   - Añadir créditos: https://platform.openai.com/account/billing
   - Crear API key: https://platform.openai.com/api-keys
   - **GUARDA tu API key** en un lugar seguro

3. **Navegador actualizado** (Chrome, Firefox, Safari, Edge)

### 🚀 OPCIONAL: Prueba el ambiente AHORA

Si quieres probar antes del workshop:

1. Ve a: [URL DE TU REPO]
2. Haz clic en el botón verde "Code"
3. Selecciona "Codespaces" → "Create codespace"
4. Espera 2-3 minutos mientras se configura automáticamente
5. En el terminal, ejecuta: `python scripts/verify_setup.py`

¡Nos vemos el [FECHA]!

Saludos,
[Tu nombre]
aromero@secture.com
```

---

## 🌅 DÍA DEL WORKSHOP - 30 MIN ANTES

### ✅ Setup Técnico

- [ ] **Proyector/pantalla funcionando**
  - Resolución adecuada para código (mínimo 1920x1080)
  - Fuente grande y legible

- [ ] **Internet estable**
  - WiFi del venue probado
  - Backup: Hotspot móvil listo

- [ ] **Tu Codespace listo**
  - Abierto y verificado
  - Todos los notebooks testeados
  - Terminal lista para demos

- [ ] **Rama solutions abierta en otra pestaña**
  - Para consultar soluciones rápido
  - Pero NO compartir pantalla de esa pestaña

- [ ] **Slack/Discord/WhatsApp del workshop creado**
  - Para compartir links rápido
  - Para que participantes hagan preguntas

### ✅ Materiales Físicos

- [ ] Lista de participantes
- [ ] Códigos QR con link al repo (impreso)
- [ ] Slides introductorias (si las tienes)
- [ ] Post-its y marcadores
- [ ] Agua y café ☕

---

## 🎬 INICIO DEL WORKSHOP (08:00-08:15)

### Bienvenida (5 min)

```
1. Presentación personal
2. Objetivos del día
3. Agenda y horarios (breaks, almuerzo)
4. Reglas del workshop:
   - Preguntas bienvenidas en cualquier momento
   - Ayudarse entre participantes
   - Código de conducta
```

### Setup Asistido (10 min)

**Proyectar en pantalla grande y guiar paso a paso:**

```
1. "Todos abren GitHub.com"
   - Verificar que todos tienen cuenta

2. "Navegan a [URL DEL REPO]"
   - Compartir link en chat
   - Mostrar código QR

3. "Botón verde Code → Codespaces → Create"
   - Esperar juntos 2-3 minutos
   - Mostrar mensaje de progreso esperado

4. "Cuando vean: 🚀 RAG Workshop Environment Ready!"
   - Aplaudir 👏

5. "Configurar API Key"
   - Mostrar en pantalla cómo hacerlo
   - cp .env.example .env
   - nano .env (o editor VSCode)
   - Pegar API key

6. "Verificar instalación"
   - python scripts/verify_setup.py
   - Todos deben ver: ✅ TODO LISTO

7. "Abrir primer notebook"
   - notebooks/00_inicio.ipynb
   - Select Kernel → Python 3.11
   - Ejecutar primera celda juntos
```

### ⚠️ Troubleshooting Común

**"Mi Codespace no inicia"**
- Verificar conexión a internet
- Reintentar: Delete codespace y crear nuevo
- Alternativa: Local setup (15 min extra)

**"No tengo créditos en OpenAI"**
- Solución temporal: Compartir API key tuya (¡cuidado!)
- O: Usar modo mock (MOCK_API_CALLS=true en .env)

**"Jupyter no abre notebooks"**
- Reload window: Ctrl+Shift+P → "Reload Window"
- O: Instalar extensión Jupyter manualmente

**"Error al importar módulos"**
```bash
# Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 🏃‍♂️ DURANTE EL WORKSHOP

### Tu Setup Ideal

**2 Pantallas/Ventanas:**

1. **Pantalla Principal (Proyector)**
   - Tu Codespace con notebook actual
   - Esto es lo que ven participantes

2. **Pantalla Secundaria (Tu laptop)**
   - Rama solutions abierta (para consultar)
   - Timer visible
   - Chat/Slack del workshop
   - Este checklist abierto

### Uso de Soluciones

**Para desbloquear participantes atascados:**

```
1. NUNCA mostrar toda la solución
2. Dar hints progresivos:
   - Hint 1: "¿Qué función necesitas llamar?"
   - Hint 2: "Mira el ejemplo en la celda anterior"
   - Hint 3: Mostrar solo 2-3 líneas clave
   - Último recurso: Mostrar solución completa
```

**Archivos de soluciones por módulo:**
- M2: `solutions/nivel_2_workshop/*.py`
- M3: `solutions/guias_instructor/NOTEBOOK_03_frameworks_guia.md`
- M4: `solutions/guias_instructor/NOTEBOOK_04_produccion_guia.md`
- M5: `solutions/guias_instructor/NOTEBOOK_05_proyecto_final_guia.md`

### Timeboxing Estricto

- ⏰ Poner timer visible para cada sección
- 5 min antes del break: "Última pregunta antes del break"
- Si alguien se atrasa mucho: Ayuda individual en break
- Priorizar que todos sigan adelante juntos

---

## 📊 CHECKPOINTS POR MÓDULO

### ✅ Módulo 0 (08:00-08:15) - Setup

**Checkpoint**: Todos ejecutaron primera celda exitosamente

```python
# Debe correr sin errores:
import openai
print("✅ Todo listo!")
```

---

### ✅ Módulo 1 (08:15-09:30) - Fundamentos

**Checkpoint 1 (08:45)**: SimpleRAG inicializado
```python
rag = SimpleRAG()
# Debe imprimir: ✅ Tu primer RAG está listo!
```

**Checkpoint 2 (09:15)**: Primera query exitosa
```python
respuesta = rag.query("¿Cuál es la política de vacaciones?")
# Debe retornar respuesta coherente
```

**Antes del break**: Todos vieron sus métricas

---

### ✅ Módulo 2 (09:45-11:15) - Optimización

**Checkpoint 1 (10:15)**: Módulos v1 y v2 comparados
```python
print(f"V1: {len(chunks_v1)} chunks")
print(f"V2: {len(chunks_v2)} chunks")
# V2 debe tener más chunks por overlap
```

**Checkpoint 2 (10:45)**: Cache funcionando
```python
# Primera ejecución: ~1000ms
# Segunda ejecución: ~50ms (cache hit)
```

**Checkpoint 3 (11:00)**: Ejercicio 1 completado
- Al menos intentaron encontrar chunk_size óptimo

---

### ✅ Módulo 3 (12:00-13:30) - Frameworks

**Checkpoint 1 (12:15)**: Path elegido
- Cada participante sabe qué path seguir (A, B, o C)

**Checkpoint 2 (13:00)**: Framework funcionando
```python
# LangChain
rag_langchain.query_with_memory("test")

# O LlamaIndex
rag_llamaindex.query_with_context("test")
```

**Antes de almuerzo**: Comparación de approaches discutida

---

### ✅ Módulo 4 (13:45-15:00) - Producción

**Checkpoint 1 (14:15)**: API iniciada localmente
```bash
python src/module_4_api.py
# Debe correr en localhost:8000
```

**Checkpoint 2 (14:45)**: Al menos 5 TODOs completados
```python
# TODO 1, 3, 6, 9, 10 son los más críticos
```

---

### ✅ Módulo 5 (15:00-15:45) - Proyecto Final

**Checkpoint 1 (15:15)**: Proyecto elegido y template personalizado
**Checkpoint 2 (15:35)**: Código básico funcionando
**Checkpoint 3 (15:45)**: Listo para presentar (aunque no esté perfecto)

---

## 🎤 PRESENTACIONES FINALES (15:45-16:00)

### Formato (3 min por persona)

```
1. Nombre y proyecto elegido (30 seg)
2. Demo rápida (1 min)
3. Desafío más grande (30 seg)
4. Aprendizaje más importante (30 seg)
5. Q&A (30 seg)
```

### Tu Rol

- Moderar tiempo estrictamente
- Hacer 1-2 preguntas constructivas
- Destacar lo bueno de cada proyecto
- Terminar con aplauso 👏

---

## 📸 CIERRE (16:00)

### Checklist Final

- [ ] Foto grupal (pedir permiso)
- [ ] Encuesta de feedback (Google Form)
- [ ] Compartir:
  - [ ] Slides/materiales adicionales
  - [ ] Link al repo para seguir practicando
  - [ ] Recursos adicionales (docs, papers, cursos)
  - [ ] Tu contacto para dudas futuras

### Mensaje de Cierre

```
"¡Felicitaciones! 🎉

En 8 horas han:
✅ Construido RAG desde cero
✅ Optimizado latencia 75%
✅ Integrado frameworks profesionales
✅ Deployado a producción
✅ Creado su propio proyecto

Esto es solo el inicio. Los recursos están en el repo
para que sigan experimentando.

¡Son oficialmente RAG Masters! 🏆

Nos mantenemos en contacto en [Slack/Discord].
¡Muchas gracias y éxito en sus proyectos!"
```

---

## 📧 POST-WORKSHOP

### Día siguiente

- [ ] Email de agradecimiento con recursos
- [ ] Compilar feedback de encuestas
- [ ] Compartir fotos (si hay permiso)
- [ ] Actualizar repo con FAQ de dudas comunes

### 1 Semana después

- [ ] Check-in: ¿Alguien implementó RAG en su proyecto?
- [ ] Ofrecer office hours para dudas
- [ ] Compartir proyectos destacados en LinkedIn

---

## 🆘 CONTACTOS DE EMERGENCIA

**Internet falla**:
- Backup: Hotspot móvil
- Plan B: Notebooks pre-ejecutados con outputs

**Proyector falla**:
- Backup: Compartir pantalla vía Zoom/Meet
- Plan C: Workshop estilo "mob programming"

**Yo me enfermo**:
- Co-instructor: [Nombre]
- Todo está documentado en este repo
- Pueden auto-guiarse con notebooks

---

## ✨ TIPS DE ENSEÑANZA

### Mantén la Energía

- Parate y camina mientras explicas
- Usa metáforas y analogías
- Celebra pequeños logros
- Breaks puntuales (la gente necesita café)

### Lectura del Salón

- Si >50% están atascados → Para y explica de nuevo
- Si >80% terminaron → Acelera o da desafío extra
- Si alguien está muy perdido → Ayuda en break

### Preguntas Frecuentes

**"¿Por qué usamos embeddings y no keywords?"**
→ Demo en vivo con ejemplos

**"¿Esto reemplaza fine-tuning?"**
→ No, son complementarios. Explicar cuándo usar cada uno

**"¿Cuánto cuesta en producción?"**
→ Mostrar calculadora de costos real

---

**¡ÉXITO EN EL WORKSHOP!** 🚀

**Última revisión**: 2025-10-01
**Instructor**: Antonio Romero
**Contacto**: aromero@secture.com
