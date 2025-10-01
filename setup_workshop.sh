#!/bin/bash

# RAG Workshop 2025 - Setup Script
# Este script configura todo el ambiente automáticamente

set -e  # Exit on error

echo "
╔══════════════════════════════════════════════════╗
║     🚀 RAG WORKSHOP 2025 - SETUP AUTOMÁTICO      ║
╚══════════════════════════════════════════════════╝
"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 1. Verificar Python
echo "🔍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION encontrado"
else
    print_error "Python 3 no encontrado. Por favor instala Python 3.11+"
    exit 1
fi

# 2. Crear estructura de directorios
echo ""
echo "📁 Creando estructura de directorios..."
mkdir -p .devcontainer
mkdir -p notebooks
mkdir -p src
mkdir -p data/{processed,vectordb,cache}
mkdir -p tests
mkdir -p logs
mkdir -p outputs
mkdir -p docs
print_status "Directorios creados"

# 3. Verificar archivos críticos
echo ""
echo "📄 Verificando archivos críticos..."

if [ ! -f "requirements.txt" ]; then
    print_warning "requirements.txt no encontrado. Creando uno básico..."
    cat > requirements.txt << 'EOF'
openai==1.45.0
chromadb==0.5.0
langchain==0.2.11
python-dotenv==1.0.0
jupyter==1.0.0
pandas==2.2.0
PyPDF2==3.0.1
fastapi==0.110.0
streamlit==1.35.0
EOF
fi

if [ ! -f ".env.example" ]; then
    print_warning ".env.example no encontrado. Creando..."
    cat > .env.example << 'EOF'
OPENAI_API_KEY=sk-YOUR-API-KEY-HERE
LOG_LEVEL=INFO
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EOF
fi

# 4. Crear ambiente virtual (opcional)
echo ""
read -p "¿Quieres crear un ambiente virtual local? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🐍 Creando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    print_status "Ambiente virtual creado y activado"
    
    echo "📦 Instalando dependencias..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_status "Dependencias instaladas"
fi

# 5. Configurar .env
echo ""
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning ".env creado desde template"
    
    read -p "¿Tienes tu API key de OpenAI? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        read -p "Ingresa tu API key: " API_KEY
        if [[ $API_KEY == sk-* ]]; then
            sed -i.bak "s/sk-YOUR-API-KEY-HERE/$API_KEY/" .env
            rm .env.bak 2>/dev/null || true
            print_status "API key configurada"
        else
            print_warning "API key no parece válida. Configúrala manualmente en .env"
        fi
    fi
else
    print_status ".env ya existe"
fi

# 6. Generar datos de ejemplo
echo ""
echo "📊 Generando datos de ejemplo..."
if [ -f "src/utils.py" ]; then
    python3 src/utils.py --create-sample-data
else
    print_warning "utils.py no encontrado. Crea los datos manualmente"
fi

# 7. Verificar instalación
echo ""
echo "🔍 Verificando instalación..."
python3 -c "
import sys
print(f'Python: {sys.version.split()[0]}')
try:
    import openai
    print('✅ OpenAI instalado')
except:
    print('❌ OpenAI no instalado')
try:
    import chromadb
    print('✅ ChromaDB instalado')
except:
    print('❌ ChromaDB no instalado')
try:
    import langchain
    print('✅ LangChain instalado')
except:
    print('❌ LangChain no instalado')
"

# 8. Crear README rápido para alumnos
echo ""
echo "📝 Creando instrucciones rápidas..."
cat > QUICK_START.md << 'EOF'
# 🚀 Quick Start - RAG Workshop

## Para Alumnos:

### Opción 1: GitHub Codespaces (Recomendado)
1. Fork este repositorio
2. Click en "Code" → "Codespaces" → "Create codespace"
3. Espera 2-3 minutos
4. ¡Listo!

### Opción 2: Local
```bash
git clone [este-repo]
cd rag-workshop-2025
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tu API key
jupyter lab
```

## Primer Paso:
Abre `notebooks/00_inicio.ipynb`

## ¿Problemas?
- Slack: #rag-workshop
- Levanta la mano
EOF
print_status "QUICK_START.md creado"

# 9. Test final
echo ""
echo "🎯 Test final del sistema..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if api_key and api_key.startswith('sk-'):
    print('✅ API Key configurada')
else:
    print('⚠️  API Key no configurada - configúrala en .env')

print('✅ Sistema listo para el workshop!')
"

# 10. Resumen final
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║           ✅ SETUP COMPLETADO                    ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║                                                  ║"
echo "║  Siguientes pasos:                              ║"
echo "║  1. Configura tu API key en .env                ║"
echo "║  2. Prueba el notebook 00_inicio.ipynb          ║"
echo "║  3. Comparte el repo con los alumnos            ║"
echo "║                                                  ║"
echo "║  Comandos útiles:                               ║"
echo "║  - jupyter lab          (iniciar notebooks)     ║"
echo "║  - python src/utils.py --validate               ║"
echo "║  - git push             (subir cambios)         ║"
echo "║                                                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "🚀 ¡Buena suerte con el workshop!"