#!/bin/bash

echo "🔧 Configurando ambiente RAG Workshop..."

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias principales
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Crear estructura de datos si no existe
echo "📂 Preparando directorios..."
mkdir -p data/processed
mkdir -p data/vectordb
mkdir -p data/cache
mkdir -p logs
mkdir -p outputs

# Configurar Jupyter
echo "📓 Configurando Jupyter..."
jupyter notebook --generate-config || true
jupyter lab --generate-config || true

# Instalar kernels adicionales
python -m ipykernel install --user --name rag-env --display-name "RAG Workshop"

# Crear archivo .env desde template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Por favor, configura tu API key en el archivo .env"
fi

# Verificar instalación
echo "✅ Verificando instalación..."
python -c "
try:
    import chromadb
    import openai
    import langchain
    import llama_index
    print('✅ Todas las librerías principales instaladas correctamente')
except ImportError as e:
    print(f'⚠️  Advertencia: {e}')
"

# Verificar que los datos de ejemplo existen
if [ ! -f data/company_handbook.pdf ]; then
    echo "⚠️  Datos de ejemplo no encontrados. Los notebooks pueden requerir configuración adicional."
fi

# Verificar API key
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY', '')
if api_key and api_key.startswith('sk-'):
    print('✅ API Key detectada (recuerda configurarla si es un placeholder)')
else:
    print('⚠️  API Key no configurada - edita el archivo .env')
"

# Mensaje de bienvenida
echo "
╔═══════════════════════════════════════════════╗
║                                               ║
║     🚀 RAG WORKSHOP 2025 - READY!            ║
║                                               ║
║  📚 Notebooks: /workspace/notebooks/         ║
║  📦 Código: /workspace/src/                  ║
║  📊 Datos: /workspace/data/                  ║
║                                               ║
║  ⚠️  Recuerda configurar tu API key en .env  ║
║                                               ║
║  Abre notebooks/00_inicio.ipynb para empezar ║
║                                               ║
╚═══════════════════════════════════════════════╝
"

echo "✅ Setup completado en $(date)"
