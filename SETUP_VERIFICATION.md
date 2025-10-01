# ✅ Guía de Verificación y Setup - Workshop RAG 2025

**Para Instructores**: Cómo verificar que todo funciona antes del workshop
**Para Participantes**: Cómo acceder al workshop (¡TODO EN LA NUBE! ☁️)

---

## 🚀 OPCIÓN 1: GitHub Codespaces (RECOMENDADA - 100% EN LA NUBE)

### ✨ **¡NO necesitan instalar NADA en su Mac!**

**Ventajas**:
- ✅ Todo configurado automáticamente
- ✅ Funciona desde el navegador
- ✅ Ambiente idéntico para todos
- ✅ No consume recursos locales
- ✅ Jupyter, VSCode, todo incluido
- ✅ Gratis para uso personal (60 horas/mes)

### 📋 Pasos para Participantes (5 minutos)

#### 1. Acceder al repositorio
```
1. Ve a: https://github.com/[TU-USUARIO]/rag-workshop-2025
2. Haz clic en el botón verde "Code"
3. Selecciona la pestaña "Codespaces"
4. Clic en "Create codespace on main"
```

#### 2. Esperar inicialización (2-3 minutos)
```
GitHub Codespaces:
✅ Creando contenedor...
✅ Instalando Python 3.11...
✅ Instalando dependencias (requirements.txt)...
✅ Configurando Jupyter...
✅ Preparando notebooks...

Mensaje final: 🚀 RAG Workshop Environment Ready!
```

#### 3. Configurar API Key de OpenAI
```bash
# En el terminal de Codespaces:
cp .env.example .env
nano .env  # o usa el editor de VSCode

# Edita esta línea:
OPENAI_API_KEY=sk-TU-API-KEY-AQUI
```

#### 4. Verificar instalación
```bash
# Ejecutar script de verificación
python scripts/verify_setup.py
```

**Output esperado**:
```
🔍 Verificando instalación...

✅ Python 3.11.9
✅ OpenAI 1.45.0
✅ LangChain 0.2.11
✅ LlamaIndex 0.10.55
✅ ChromaDB 0.5.0
✅ FastAPI 0.110.0
✅ Jupyter instalado

✅ API Key configurada
✅ Conexión con OpenAI exitosa (latencia: 234ms)
✅ Archivos de datos encontrados (4/4)

🎉 TODO LISTO PARA EL WORKSHOP!
```

#### 5. Abrir primer notebook
```
1. En el explorador de archivos (izquierda)
2. Navegar a: notebooks/00_inicio.ipynb
3. Hacer doble clic para abrir
4. Clic en "Select Kernel" → Python 3.11.x
5. Ejecutar primera celda (Shift + Enter)
```

---

## 🔧 OPCIÓN 2: Instalación Local en Mac (ALTERNATIVA)

Solo si Codespaces no está disponible o prefieren local.

### Prerequisitos
- macOS 10.15+
- Homebrew instalado
- Python 3.11+

### Instalación (15-20 minutos)

```bash
# 1. Clonar repositorio
git clone https://github.com/[TU-USUARIO]/rag-workshop-2025.git
cd rag-workshop-2025

# 2. Crear ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configurar API Key
cp .env.example .env
nano .env  # Editar OPENAI_API_KEY

# 5. Verificar instalación
python scripts/verify_setup.py

# 6. Iniciar Jupyter
jupyter lab
```

---

## 🧪 Script de Verificación Completo

Voy a crear un script que verifica TODA la instalación:

