# 🔧 Troubleshooting - RAG Workshop 2025

Guía completa para resolver problemas comunes durante el workshop.

---

## 🚨 Problemas Comunes

### 1. API Key Inválida o No Configurada

**Error:**
```
AuthenticationError: Invalid API key provided
```

**Solución:**
1. Verifica que tu `.env` tiene el formato correcto:
   ```bash
   OPENAI_API_KEY=sk-proj-...tu-key-aquí
   ```
2. NO uses comillas, NO uses espacios extras
3. Recarga el ambiente en el notebook:
   ```python
   from dotenv import load_dotenv
   load_dotenv(override=True)
   ```
4. Verifica tu key en: https://platform.openai.com/api-keys

---

### 2. Sin Créditos en OpenAI

**Error:**
```
RateLimitError: You exceeded your current quota
```

**Solución:**
1. Verifica tu balance: https://platform.openai.com/account/usage
2. Añade créditos: https://platform.openai.com/account/billing
3. Mínimo recomendado: $5 USD
4. Si acabas de añadir créditos, espera 5-10 minutos

---

### 3. ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'chromadb'
```

**Solución:**
```bash
# Reinstalar todas las dependencias
pip install -r requirements.txt --upgrade

# O instalar la específica
pip install chromadb==0.5.0
```

---

### 4. Codespace No Carga / Muy Lento

**Síntomas:**
- Pantalla blanca después de 5+ minutos
- "Configuring..." infinito

**Solución:**
1. **Refresca el navegador** (Ctrl+F5 / Cmd+Shift+R)
2. Si persiste, **elimina y recrea el Codespace**:
   - Ve a GitHub → Code → Codespaces
   - Click en "..." → Delete
   - Crea uno nuevo
3. Usa **Chrome o Firefox** (mejor compatibilidad)
4. Verifica tu conexión a internet

---

### 5. Notebook No Encuentra Archivos

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/company_handbook.pdf'
```

**Solución:**
1. Verifica que los archivos existen:
   ```bash
   ls -la data/
   ```
2. Si faltan, descárgalos del repositorio:
   ```bash
   git pull origin main
   ```
3. O regenera manualmente:
   ```bash
   python src/utils.py --create-sample-data
   ```

---

### 6. ChromaDB: "Collection already exists"

**Error:**
```
Exception: Collection rag_workshop_2025 already exists
```

**Solución:**
```python
# Opción 1: Usar colección existente
collection = client.get_collection("rag_workshop_2025")

# Opción 2: Eliminar y recrear
client.delete_collection("rag_workshop_2025")
collection = client.create_collection("rag_workshop_2025")

# Opción 3: Limpiar todo
import shutil
shutil.rmtree("data/vectordb")
```

---

### 7. Kernel Jupyter Muerto

**Síntomas:**
- Celda ejecutándose infinitamente
- Mensaje "Kernel has died"

**Solución:**
1. **Reiniciar kernel**: Menú → Kernel → Restart Kernel
2. Si persiste:
   ```bash
   # En terminal
   pip install --upgrade ipykernel jupyter
   python -m ipykernel install --user --name rag-env
   ```
3. Cierra y reabre el notebook

---

### 8. Importación Lenta / Timeout

**Síntomas:**
- Primera celda tarda 2+ minutos
- Timeout en imports

**Causas comunes:**
- Primera vez que se cargan modelos de sentence-transformers
- Descarga de modelos en background

**Solución:**
- **Es normal la primera vez**
- Espera pacientemente (puede ser 3-5 minutos)
- Los siguientes runs serán rápidos

---

### 9. Error de Permisos en Codespaces

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solución:**
```bash
# Cambiar permisos de directorios
chmod -R 755 data/
chmod -R 755 logs/
chmod -R 755 outputs/
```

---

### 10. Git: "Changes not staged"

**Síntomas:**
- No puedes hacer git pull
- Archivos modificados localmente

**Solución:**
```bash
# Guardar tus cambios
git stash

# Actualizar
git pull origin main

# Recuperar tus cambios
git stash pop
```

---

## 💡 Tips Generales

### Antes de Pedir Ayuda

1. **Lee el mensaje de error completo**
2. **Busca el error en este documento**
3. **Intenta reiniciar el kernel/notebook**
4. **Verifica variables de entorno**

### Comandos de Diagnóstico

```python
# Verificar instalación
import sys
print(f"Python: {sys.version}")

import openai
print(f"OpenAI: {openai.__version__}")

import chromadb
print(f"ChromaDB: {chromadb.__version__}")

# Verificar API key
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("OPENAI_API_KEY", "")
print(f"API Key configurada: {key[:10]}..." if key else "❌ No configurada")

# Verificar archivos
from pathlib import Path
data_dir = Path("data")
print(f"Archivos en data/: {list(data_dir.glob('*'))}")
```

---

## 🆘 Soporte en Vivo (Durante el Workshop)

- 💬 **Slack**: #rag-workshop-2025
- 🙋 **Levanta la mano** (virtual/presencial)
- 👥 **Pregunta a tu compañero** (pair debugging)

## 📧 Soporte Post-Workshop

- **Email**: aromero@secture.com
- **Tiempo de respuesta**: 24-48 horas
- **Incluye en tu mensaje**:
  - Descripción del problema
  - Mensaje de error completo
  - Pasos que ya intentaste
  - Screenshot si aplica

---

## 🔍 Logs de Debug

Si necesitas investigar más:

```bash
# Ver logs de instalación
cat logs/setup.log

# Ver logs de la aplicación
cat logs/app.log

# Verificar variables de entorno
env | grep -i openai
```

---

## ✅ Verificación de Salud del Sistema

Copia y ejecuta este script en un notebook para diagnóstico completo:

```python
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA\n")
print("="*50)

# Python
print(f"✅ Python: {sys.version.split()[0]}")

# Librerías
try:
    import openai
    print(f"✅ OpenAI: {openai.__version__}")
except Exception as e:
    print(f"❌ OpenAI: {e}")

try:
    import chromadb
    print(f"✅ ChromaDB: {chromadb.__version__}")
except Exception as e:
    print(f"❌ ChromaDB: {e}")

try:
    import langchain
    print(f"✅ LangChain: {langchain.__version__}")
except Exception as e:
    print(f"❌ LangChain: {e}")

# API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", "")
if api_key and api_key.startswith("sk-"):
    print(f"✅ API Key: {api_key[:15]}...")
else:
    print("❌ API Key: No configurada o inválida")

# Archivos
data_dir = Path("data")
required_files = [
    "company_handbook.pdf",
    "technical_docs.pdf",
    "faqs.json",
    "support_tickets.csv"
]

for file in required_files:
    if (data_dir / file).exists():
        print(f"✅ {file} existe")
    else:
        print(f"❌ {file} faltante")

print("\n" + "="*50)
print("Diagnóstico completado. Si hay ❌, revisa las soluciones arriba.")
```

---

**¿No encuentras la solución?** → aromero@secture.com
