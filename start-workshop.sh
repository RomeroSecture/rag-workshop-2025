#!/bin/bash

# ============================================
# RAG Workshop 2025 - Inicio Rápido con Docker
# ============================================

set -e

echo "🚀 RAG Workshop 2025 - Configuración con Docker"
echo "================================================"
echo ""

# Verificar Docker instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "📥 Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    echo "📥 Instala Docker Compose desde: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker detectado: $(docker --version)"
echo ""

# Verificar .env
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita el archivo .env y añade tu OPENAI_API_KEY"
    echo "   Puedes obtener tu API key en: https://platform.openai.com/api-keys"
    echo ""
    read -p "Presiona Enter cuando hayas configurado tu API key..."
fi

# Verificar API key configurada
if grep -q "your-api-key-here" .env; then
    echo ""
    echo "⚠️  ADVERTENCIA: No has configurado tu OPENAI_API_KEY"
    echo "   El workshop no funcionará sin una API key válida"
    echo ""
    read -p "¿Continuar de todas formas? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelado. Configura tu API key en .env y vuelve a ejecutar este script."
        exit 0
    fi
fi

echo ""
echo "🔨 Construyendo imagen Docker..."
docker-compose build

echo ""
echo "🚀 Iniciando servicios..."
docker-compose up -d

echo ""
echo "⏳ Esperando que Jupyter Lab esté listo..."
sleep 5

echo ""
echo "✅ ¡Workshop listo!"
echo ""
echo "📊 Servicios disponibles:"
echo "  🔬 Jupyter Lab:   http://localhost:8888"
echo "  🎨 Streamlit:     http://localhost:8501"
echo "  ⚡ FastAPI:       http://localhost:8000"
echo "  🎭 Gradio:        http://localhost:7860"
echo "  💾 ChromaDB:      http://localhost:8001"
echo ""
echo "🛠️  Comandos útiles:"
echo "  - Ver logs:       docker-compose logs -f"
echo "  - Detener:        docker-compose down"
echo "  - Reiniciar:      docker-compose restart"
echo "  - Shell:          docker-compose exec jupyter bash"
echo ""
echo "📘 Abre tu navegador en: http://localhost:8888"
echo ""
