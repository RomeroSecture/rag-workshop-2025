# 🚀 Quickstart Guide - GitHub Codespaces

**🐍 Ambiente**: Python 3.11 con todas las dependencias pre-instaladas
**📘 Más detalles**: Ver [ENVIRONMENT.md](ENVIRONMENT.md)

## ⚡ Setup Rápido (5 minutos)

### 1️⃣ Configurar API Key

**IMPORTANTE:** Necesitas una API key de OpenAI para el workshop.

```bash
# Copiar template de .env
cp .env.example .env

# Editar .env y añadir tu API key
# Reemplaza 'your-api-key-here' con tu API key real
```

Tu `.env` debería verse así:
```bash
OPENAI_API_KEY=sk-proj-...tu-key-real-aqui...
```

**¿Dónde conseguir tu API key?**
- 🔗 https://platform.openai.com/api-keys
- ✅ Asegúrate de tener créditos (mínimo $5 USD)

---

### 2️⃣ Verificar Instalación

Las dependencias deberían instalarse automáticamente. Para verificar:

```bash
# Opción A: Verificar con Python
python3 -c "import openai, chromadb, langchain; print('✅ Todo instalado!')"

# Opción B: Ejecutar el notebook
# Abre notebooks/00_inicio.ipynb y ejecuta las primeras celdas
```

**Si ves errores de importación:**

```bash
# Instalar dependencias manualmente
pip install -r requirements.txt

# Esto toma 2-3 minutos
```

---

### 3️⃣ Abrir Notebooks

```bash
# Navegar a carpeta de notebooks
cd notebooks

# Abrir Jupyter Lab (recomendado)
jupyter lab

# O abrir directamente los archivos .ipynb en VS Code
```

**Orden recomendado:**
1. `00_inicio.ipynb` - Verificación y setup
2. `01_fundamentos.ipynb` - Módulo 1
3. `02_arquitectura.ipynb` - Módulo 2
4. `03_frameworks.ipynb` - Módulo 3
5. `04_produccion.ipynb` - Módulo 4
6. `05_proyecto_final.ipynb` - Proyecto final

---

## 🔍 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'openai'"

**Solución:**
```bash
pip install -r requirements.txt
```

Luego **reinicia el kernel** del notebook:
- Kernel → Restart Kernel
- Re-ejecuta las celdas

---

### ❌ "AuthenticationError: Invalid API key"

**Solución:**
1. Verifica que copiaste tu API key completa
2. Asegúrate de que empiece con `sk-proj-` o `sk-`
3. Revisa que no haya espacios al inicio/final
4. Recarga las variables de entorno:

```python
from dotenv import load_dotenv
load_dotenv(override=True)
```

---

### ❌ "RateLimitError: You exceeded your current quota"

**Solución:**
1. Ve a https://platform.openai.com/account/billing
2. Añade créditos (mínimo $5 USD)
3. Espera 5-10 minutos para que se procesen
4. Intenta de nuevo

---

### ❌ Jupyter no muestra cambios después de instalar

**Solución:**
```python
# En el notebook, ejecuta:
import sys
sys.path.insert(0, '/workspace')

# O reinicia completamente el kernel:
# Kernel → Restart Kernel & Clear Output
```

---

## 📂 Estructura del Proyecto

```
rag-workshop-2025/
├── notebooks/              # 📓 Tus notebooks de trabajo
│   ├── 00_inicio.ipynb     # ← EMPIEZA AQUÍ
│   ├── 01_fundamentos.ipynb
│   ├── 02_arquitectura.ipynb
│   ├── 03_frameworks.ipynb
│   ├── 04_produccion.ipynb
│   └── 05_proyecto_final.ipynb
│
├── src/                    # 📦 Código modular
│   ├── shared_config.py
│   ├── module_1_basics.py
│   ├── module_2_optimized.py
│   └── ...
│
├── data/                   # 📊 Datos de ejemplo
│   └── company_handbook.pdf  # PDF completo (13 páginas)
│
├── requirements.txt        # 📋 Dependencias Python
├── .env.example           # 🔐 Template de configuración
└── .env                   # 🔑 TU configuración (crear)
```

---

## ✅ Checklist de Preparación

Antes de empezar el workshop, asegúrate de tener:

- [ ] ✅ API Key de OpenAI configurada en `.env`
- [ ] ✅ Créditos en tu cuenta OpenAI (mínimo $5)
- [ ] ✅ Dependencias instaladas (`pip list | grep openai`)
- [ ] ✅ Notebook 00 ejecutándose sin errores
- [ ] ✅ Archivo `data/company_handbook.pdf` presente

**Test rápido:**
```bash
python3 << 'EOF'
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say: RAG Workshop Ready!"}],
    max_tokens=10
)

print(f"✅ {response.choices[0].message.content}")
print(f"💰 Tokens usados: {response.usage.total_tokens}")
EOF
```

Si ves "✅ RAG Workshop Ready!" - **¡ESTÁS LISTO!** 🎉

---

## 💡 Tips para Codespaces

### Optimizar rendimiento:
```bash
# Usar extensión Python de VS Code
# Debería auto-detectar el environment

# Si es lento, aumenta machine type:
# Codespace → Change machine type → 4-core o 8-core
```

### Guardar tu trabajo:
- ✅ Los cambios se guardan automáticamente
- ✅ Commits se sincronizan con GitHub
- ⚠️ Los Codespaces se pausan después de 30 min de inactividad
- ⚠️ Se eliminan después de 30 días sin uso

### Exportar notebooks:
```bash
# Descargar un notebook
# Click derecho en archivo → Download

# O usar GitHub para pull
git add .
git commit -m "Mi progreso del workshop"
git push
```

---

## 🆘 Necesitas Ayuda?

### Durante el workshop:
- 🙋 Levanta la mano
- 💬 Pregunta en Slack: `#workshop-rag-2025`
- 👥 Pide ayuda a tu vecino

### Recursos:
- 📚 [OpenAI Docs](https://platform.openai.com/docs)
- 📖 [Jupyter Docs](https://jupyter.org/documentation)
- 🐍 [Python Docs](https://docs.python.org/3/)

### Contacto:
- 📧 Email: aromero@secture.com
- 🐛 Issues: [GitHub Issues](https://github.com/RomeroSecture/rag-workshop-2025/issues)

---

**¡Nos vemos en el workshop! 🚀**
