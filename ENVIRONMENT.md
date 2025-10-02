# 🐍 Configuración del Ambiente - RAG Workshop 2025

## 📋 Resumen

Este workshop usa **Python 3.11** en GitHub Codespaces para garantizar compatibilidad con todas las dependencias de IA.

## 🎯 ¿Por qué Python 3.11?

- ✅ **Máxima Compatibilidad**: Todas las librerías de LangChain, LlamaIndex y ChromaDB están probadas con Python 3.11
- ✅ **Estabilidad**: Python 3.11 es la versión más estable para proyectos de producción RAG
- ✅ **Sin Conflictos**: Evita problemas de dependencias que ocurren con Python 3.12+ o 3.13

## 🚀 Ambiente en GitHub Codespaces

Cuando abres este repositorio en GitHub Codespaces:

1. **Automáticamente se crea** un contenedor Docker con Python 3.11
2. **Se instalan todas las dependencias** del archivo `requirements.txt`
3. **Jupyter Lab queda listo** para ejecutar los notebooks

### Verificar tu Versión de Python

```bash
python --version
# Debe mostrar: Python 3.11.x
```

## 📦 Dependencias Instaladas

### Core IA
- OpenAI SDK 1.45.0
- Anthropic 0.34.0
- Cohere 5.9.3

### Frameworks RAG
- **LangChain** 0.3.7 (+ Community, OpenAI, Chroma extensions)
- **LangGraph** 0.2.45 (para agentes multi-step)
- **LlamaIndex** 0.11.20 (+ OpenAI, Chroma integrations)

### Vector Databases
- ChromaDB 0.5.5
- FAISS 1.8.0
- Pinecone 5.0.1
- Qdrant 1.11.3

### Document Processing
- PyPDF2, pdfplumber (PDFs)
- python-docx (Word)
- pandas, openpyxl (Excel/CSV)
- BeautifulSoup4 (HTML)

### Web Frameworks
- FastAPI 0.115.5
- Streamlit 1.40.1
- Gradio 5.5.0

## 🔧 Instalación Manual (si es necesario)

Si por alguna razón las dependencias no se instalaron automáticamente:

```bash
# En el terminal de Codespaces
pip install -r requirements.txt
```

O desde un notebook:

```python
import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"])
```

## 🏠 Trabajando Localmente (Opcional)

Si prefieres trabajar en tu máquina local:

### Opción 1: Usar Python 3.11

```bash
# Instalar pyenv (gestor de versiones)
curl https://pyenv.run | bash

# Instalar Python 3.11
pyenv install 3.11.9
pyenv local 3.11.9

# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Opción 2: Usar Docker

```bash
# Construir imagen
docker build -t rag-workshop .

# Ejecutar contenedor
docker run -p 8888:8888 -v $(pwd):/workspace rag-workshop
```

## ⚠️ Problemas Comunes

### "ModuleNotFoundError" en los Notebooks

**Causa**: El kernel de Jupyter no está usando el Python correcto.

**Solución**:
1. En Jupyter Lab: `Kernel` → `Change Kernel` → Seleccionar `Python 3.11`
2. O ejecutar en una celda:

```python
import sys
print(f"Python: {sys.version}")
print(f"Ejecutable: {sys.executable}")
```

### Conflictos de Versiones

**Causa**: Tienes Python 3.12+ o 3.13 instalado localmente.

**Solución**: Usa GitHub Codespaces (recomendado) o cambia a Python 3.11.

### Instalación Lenta

**Causa**: Algunas librerías (como sentence-transformers) descargan modelos grandes.

**Solución**: Es normal. La primera instalación puede tomar 5-10 minutos.

## 📊 Verificación Completa del Ambiente

Ejecuta este código en un notebook para verificar todo:

```python
import sys
print(f"✅ Python: {sys.version}")

# Verificar Core Dependencies
try:
    import openai
    print(f"✅ OpenAI: {openai.__version__}")
except ImportError as e:
    print(f"❌ OpenAI: {e}")

try:
    import chromadb
    print(f"✅ ChromaDB: {chromadb.__version__}")
except ImportError as e:
    print(f"❌ ChromaDB: {e}")

try:
    import langchain
    print(f"✅ LangChain: {langchain.__version__}")
except ImportError as e:
    print(f"❌ LangChain: {e}")

try:
    import llama_index
    print(f"✅ LlamaIndex: {llama_index.__version__}")
except ImportError as e:
    print(f"❌ LlamaIndex: {e}")

print("\n🎉 Ambiente listo para el workshop!")
```

## 🆘 Soporte

Si encuentras problemas:

1. Verifica que estés en GitHub Codespaces con Python 3.11
2. Revisa [CODESPACE_QUICKSTART.md](CODESPACE_QUICKSTART.md)
3. Ejecuta el reinstall script: `bash reinstall-dependencies.sh`
4. Contacta al instructor

---

**🎓 RAG Workshop 2025** - Optimizado para aprendizaje y producción
