@echo off
REM ============================================
REM RAG Workshop 2025 - Inicio Rápido con Docker
REM ============================================

echo.
echo 🚀 RAG Workshop 2025 - Configuración con Docker
echo ================================================
echo.

REM Verificar Docker instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker no está instalado
    echo 📥 Instala Docker desde: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

docker compose version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker Compose no está instalado
    echo 📥 Instala Docker Desktop que incluye Compose
    pause
    exit /b 1
)

echo ✅ Docker detectado
docker --version
echo.

REM Verificar .env
if not exist .env (
    echo 📝 Creando archivo .env desde .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANTE: Edita el archivo .env y añade tu OPENAI_API_KEY
    echo    Puedes obtener tu API key en: https://platform.openai.com/api-keys
    echo.
    pause
)

REM Verificar API key configurada
findstr /C:"your-api-key-here" .env >nul
if not errorlevel 1 (
    echo.
    echo ⚠️  ADVERTENCIA: No has configurado tu OPENAI_API_KEY
    echo    El workshop no funcionará sin una API key válida
    echo.
    set /p continue="¿Continuar de todas formas? (S/N): "
    if /i not "%continue%"=="S" (
        echo Cancelado. Configura tu API key en .env y vuelve a ejecutar este script.
        pause
        exit /b 0
    )
)

echo.
echo 🔨 Construyendo imagen Docker...
docker-compose build

echo.
echo 🚀 Iniciando servicios...
docker-compose up -d

echo.
echo ⏳ Esperando que Jupyter Lab esté listo...
timeout /t 5 /nobreak >nul

echo.
echo ✅ ¡Workshop listo!
echo.
echo 📊 Servicios disponibles:
echo   🔬 Jupyter Lab:   http://localhost:8888
echo   🎨 Streamlit:     http://localhost:8501
echo   ⚡ FastAPI:       http://localhost:8000
echo   🎭 Gradio:        http://localhost:7860
echo   💾 ChromaDB:      http://localhost:8001
echo.
echo 🛠️  Comandos útiles:
echo   - Ver logs:       docker-compose logs -f
echo   - Detener:        docker-compose down
echo   - Reiniciar:      docker-compose restart
echo   - Shell:          docker-compose exec jupyter bash
echo.
echo 📘 Abre tu navegador en: http://localhost:8888
echo.
pause
