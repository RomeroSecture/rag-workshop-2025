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
mkdir -p logs
mkdir -p outputs

# Configurar Jupyter
echo "📓 Configurando Jupyter..."
jupyter notebook --generate-config
jupyter lab --generate-config

# Instalar kernels adicionales
python -m ipykernel install --user --name rag-env --display-name "RAG Workshop"

# Configurar Git
git config --global user.name "Workshop User"
git config --global user.email "workshop@rag.dev"
git config --global init.defaultBranch main

# Descargar modelos de spaCy si es necesario
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm

# Crear archivo .env desde template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Por favor, configura tu API key en el archivo .env"
fi

# Verificar instalación
echo "✅ Verificando instalación..."
python -c "import chromadb; import openai; import langchain; print('✅ Todas las librerías instaladas correctamente')"

# Crear datos de ejemplo si no existen
if [ ! -f data/company_handbook.pdf ]; then
    echo "📄 Generando documentos de ejemplo..."
    python src/utils.py --create-sample-data
fi

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
╚═══════════════════════════════════════════════╝
"

# Abrir primer notebook automáticamente
echo "🎯 Abriendo notebook de inicio..."
code notebooks/00_inicio.ipynb