# 🚀 Guía Rápida de Inicio - Workshop RAG 2025

## Para Participantes: **5 Minutos para Empezar** ⏱️

**¡TODO EN LA NUBE! No necesitas instalar nada en tu computadora** ☁️

---

## ✅ Pre-requisitos (Haz esto ANTES del workshop)

### 1. Cuenta de GitHub (Gratis)
```
Si no tienes → https://github.com/signup
```

### 2. API Key de OpenAI (~$5 USD de créditos)
```
1. Crea cuenta → https://platform.openai.com/signup
2. Añade $5 USD → Settings → Billing → Add payment method
3. Crea API key → https://platform.openai.com/api-keys
4. GUARDA la key (empieza con "sk-...")
```

**¿Por qué $5?** El workshop consume ~$2-3 USD en total. Sobran $2 para practicar después.

---

## 🚀 Inicio Rápido (Durante el workshop)

### PASO 1: Abrir en Codespaces (2 minutos)

```
1. Ve a: [URL DEL REPOSITORIO]
   (El instructor compartirá el link)

2. Haz clic en el botón verde "Code"

3. Pestaña "Codespaces" → "Create codespace on main"

4. ESPERA mientras se configura (2-3 minutos)
   ⏳ Instalando Python...
   ⏳ Instalando librerías...
   ⏳ Configurando Jupyter...

5. Verás: "🚀 RAG Workshop Environment Ready!"
```

**¡Listo! Ya tienes VS Code + Python + Jupyter + TODO instalado en la nube**

---

### PASO 2: Configurar tu API Key (1 minuto)

En el terminal de Codespaces (parte inferior):

```bash
# 1. Copiar template
cp .env.example .env

# 2. Editar el archivo (opción A: terminal)
nano .env

# O (opción B: usar editor VSCode)
# Hacer clic en .env en el explorador de archivos
```

**Edita esta línea:**
```
OPENAI_API_KEY=sk-TU-API-KEY-AQUI
```

**Guardar**:
- Nano: `Ctrl+O` → Enter → `Ctrl+X`
- VSCode: `Cmd+S` (Mac) o `Ctrl+S` (Windows)

---

### PASO 3: Verificar Instalación (1 minuto)

En el terminal:

```bash
python scripts/verify_setup.py
```

**Debes ver**:
```
🔍 VERIFICACIÓN DE SETUP - RAG WORKSHOP 2025
=============================================================

1️⃣ Python Version
✅ Python 3.11.9

2️⃣ Paquetes Instalados
✅ openai              1.45.0
✅ langchain           0.2.11
✅ llama-index         0.10.55
✅ chromadb            0.5.0
...
📊 Instalados: 8/8

5️⃣ OpenAI API Key
✅ Configurada: sk-proj-...

6️⃣ Conexión con OpenAI
ℹ️  Probando conexión...
✅ Conexión exitosa (latencia: 234ms)

🎉 TODO LISTO PARA EL WORKSHOP!
```

**Si algo falla**, levanta la mano y un instructor te ayudará.

---

### PASO 4: Abrir Primer Notebook (1 minuto)

```
1. En el explorador de archivos (izquierda):
   📁 notebooks/ → 00_inicio.ipynb

2. Hacer doble clic

3. Arriba a la derecha: "Select Kernel"
   → Seleccionar "Python 3.11.x" o "RAG Workshop"

4. Ejecutar primera celda:
   Shift + Enter
```

**Debe aparecer**:
```python
✅ Python 3.11.9
✅ OpenAI 1.45.0
✅ ChromaDB 0.5.0
...
✨ Ambiente verificado!
```

---

## 🎉 ¡LISTO! Estás dentro del Workshop

**Ahora solo sigue las instrucciones del instructor** 👨‍🏫

---

## ⚠️ Troubleshooting Rápido

### "Mi Codespace se atoró creando"
```
1. Espera 5 minutos completos
2. Si sigue atorado: Delete codespace
3. Crear uno nuevo
4. Si persiste: Levanta la mano
```

### "No puedo crear Codespace"
```
Error: "You've reached your limit"
→ Tienes el límite de 2 codespaces activos
→ Borra uno viejo en: https://github.com/codespaces
```

### "Mi API key no funciona"
```
1. Verifica que empiece con "sk-proj-" o "sk-"
2. Verifica que la copiaste completa (sin espacios)
3. Verifica que tienes créditos en OpenAI:
   https://platform.openai.com/account/billing
```

### "Jupyter no abre el notebook"
```
1. Ctrl+Shift+P (Cmd+Shift+P en Mac)
2. Escribir: "Reload Window"
3. Enter
4. Intentar abrir notebook de nuevo
```

### "ImportError al ejecutar celdas"
```bash
# En terminal:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 💡 Tips Útiles

### Atajos de Teclado en Jupyter

```
Shift + Enter  →  Ejecutar celda y avanzar
Ctrl + Enter   →  Ejecutar celda sin avanzar
Esc + B        →  Insertar celda abajo
Esc + A        →  Insertar celda arriba
Esc + DD       →  Eliminar celda
Tab            →  Autocompletar
Shift + Tab    →  Ver documentación
```

### Panel de Terminal

```
Ctrl + `  (backtick)  →  Toggle terminal
Ctrl + Shift + `      →  Nuevo terminal
```

### Guardar tu Trabajo

- **Automático**: Los notebooks se guardan automáticamente cada 2 minutos
- **Manual**: `Cmd+S` (Mac) o `Ctrl+S` (Windows/Linux)
- **En la nube**: Todo se guarda en tu Codespace (persiste por 30 días de inactividad)

---

## 📱 ¿Necesitas Ayuda Durante el Workshop?

1. **Levanta la mano** 🙋 - Un instructor vendrá
2. **Pregunta en el chat** del workshop (Slack/Discord/WhatsApp)
3. **Ayuda a tu vecino** - ¡colaboración bienvenida!

---

## 🎓 Después del Workshop

### Tu Codespace se queda por 30 días

```
Puedes volver cuando quieras:
1. Ve a: https://github.com/codespaces
2. Haz clic en tu codespace
3. Continúa donde lo dejaste
```

### Exportar tu Trabajo

```bash
# Descargar archivos modificados
File → Download → [archivo que quieres]

# O clonar a tu Mac:
git clone https://github.com/[TU-USUARIO]/rag-workshop-2025.git
```

### Seguir Practicando

- El repo sigue ahí con todos los materiales
- Notebooks tienen soluciones comentadas
- Puedes modificar y experimentar sin límites

---

## 📚 Recursos Adicionales

**Documentación**:
- [OpenAI API Docs](https://platform.openai.com/docs)
- [LangChain Docs](https://python.langchain.com/)
- [LlamaIndex Docs](https://docs.llamaindex.ai/)

**Comunidad**:
- Slack del workshop: [link]
- GitHub Issues: Para preguntas post-workshop

**Instructor**:
- Email: aromero@secture.com
- LinkedIn: [perfil]

---

## ✨ ¡Disfruta el Workshop!

**Recuerda**: La mejor manera de aprender es haciendo. No tengas miedo de:
- Experimentar con el código
- Romper cosas (puedes recrear el Codespace)
- Hacer preguntas "tontas" (no existen)
- Compartir tus descubrimientos

**¡Vamos a construir algo increíble juntos!** 🚀

---

**Última actualización**: 2025-10-01
**Versión**: 1.0
