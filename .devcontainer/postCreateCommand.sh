#!/bin/bash

echo "🔧 Configurando ambiente RAG Workshop..."

# Asegurar que .local/bin está en PATH
export PATH="/home/vscode/.local/bin:$PATH"

# Añadir al bashrc para sesiones futuras
if ! grep -q "/home/vscode/.local/bin" ~/.bashrc; then
    echo 'export PATH="/home/vscode/.local/bin:$PATH"' >> ~/.bashrc
fi

# Asegurar que usamos el Python correcto
PYTHON_CMD=$(which python3)
echo "🐍 Usando Python: $PYTHON_CMD"
echo "📍 PATH actualizado: $PATH"

# Actualizar pip en el Python del sistema
$PYTHON_CMD -m pip install --upgrade pip

# Instalar dependencias principales en el Python del sistema
echo "📦 Instalando dependencias..."
$PYTHON_CMD -m pip install -r requirements.txt

# Verificar que se instalaron correctamente
echo "🔍 Verificando instalación..."
$PYTHON_CMD -c "import sys; print(f'Python path: {sys.executable}')"
$PYTHON_CMD -c "import openai; print(f'OpenAI: {openai.__version__}')"
$PYTHON_CMD -c "import chromadb; print(f'ChromaDB: {chromadb.__version__}')"

# Crear estructura de datos si no existe
echo "📂 Preparando directorios..."
mkdir -p data/processed
mkdir -p data/vectordb
mkdir -p data/cache
mkdir -p logs
mkdir -p outputs

# Configurar Jupyter
echo "📓 Configurando Jupyter..."
$PYTHON_CMD -m jupyter notebook --generate-config || true
$PYTHON_CMD -m jupyter lab --generate-config || true

# Instalar kernel de Jupyter usando el mismo Python
echo "🎯 Instalando Jupyter kernel..."
$PYTHON_CMD -m ipykernel install --user --name python3 --display-name "Python 3 (RAG Workshop)"

# Verificar que el kernel tiene acceso a las librerías
echo "✅ Verificando kernel..."
$PYTHON_CMD -c "
import sys
import json
kernel_path = f'{sys.prefix}/share/jupyter/kernels/python3/kernel.json'
print(f'Kernel configurado en: {kernel_path}')
"

# Crear archivo .env desde template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Por favor, configura tu API key en el archivo .env"
fi

# Verificar instalación detallada
echo ""
echo "═══════════════════════════════════════════════"
echo "🔍 VERIFICACIÓN FINAL DE INSTALACIÓN"
echo "═══════════════════════════════════════════════"

$PYTHON_CMD -c "
import sys
print(f'🐍 Python: {sys.version}')
print(f'📍 Ubicación: {sys.executable}')
print()

# Verificar cada librería principal
libraries = ['openai', 'chromadb', 'langchain', 'llama_index', 'fastapi', 'jupyter']
failed = []

for lib in libraries:
    try:
        mod = __import__(lib)
        version = getattr(mod, '__version__', 'unknown')
        print(f'✅ {lib:15s} {version}')
    except ImportError as e:
        print(f'❌ {lib:15s} NO INSTALADO')
        failed.append(lib)

print()
if not failed:
    print('✅ TODAS LAS LIBRERÍAS INSTALADAS CORRECTAMENTE')
else:
    print(f'⚠️  FALTAN: {', '.join(failed)}')
    print('   Ejecuta: pip install -r requirements.txt')
"
echo "═══════════════════════════════════════════════"

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

# Crear script de reinstalación por si acaso
cat > /workspace/reinstall-dependencies.sh << 'REINSTALL'
#!/bin/bash
echo "🔄 Reinstalando dependencias del RAG Workshop..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt --force-reinstall
echo "✅ Reinstalación completada. Reinicia el kernel de Jupyter."
REINSTALL

chmod +x /workspace/reinstall-dependencies.sh

echo ""
echo "✅ Setup completado en $(date)"
echo ""
echo "💡 Si encuentras problemas con las librerías:"
echo "   Ejecuta: bash reinstall-dependencies.sh"
echo ""
