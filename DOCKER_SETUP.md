# 🐳 RAG Workshop 2025 - Setup con Docker

**⚡ Opción recomendada para máxima estabilidad y facilidad**

## 🎯 Ventajas de usar Docker

- ✅ **Sin problemas de versiones** - Ambiente 100% consistente
- ✅ **Python 3.11 garantizado** - No importa tu Python local
- ✅ **Todo pre-instalado** - Todas las dependencias listas
- ✅ **Multiplataforma** - Windows, Mac, Linux
- ✅ **Sin conflictos** - Ambiente aislado de tu sistema
- ✅ **Fácil limpieza** - Borra el contenedor cuando termines

---

## 📦 Instalación de Docker

### Windows
1. Descarga [Docker Desktop para Windows](https://docs.docker.com/desktop/install/windows-install/)
2. Ejecuta el instalador
3. Reinicia tu computadora
4. Verifica: `docker --version` en PowerShell

### macOS
1. Descarga [Docker Desktop para Mac](https://docs.docker.com/desktop/install/mac-install/)
2. Arrastra Docker.app a Aplicaciones
3. Abre Docker Desktop
4. Verifica: `docker --version` en Terminal

### Linux (Ubuntu/Debian)
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Añadir tu usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Instalar Docker Compose
sudo apt-get install docker-compose-plugin

# Verificar
docker --version
docker compose version
```

---

## 🚀 Inicio Rápido (3 pasos)

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/[tu-usuario]/rag-workshop-2025.git
cd rag-workshop-2025
```

### 2️⃣ Configurar API Key

```bash
# Copiar template
cp .env.example .env

# Editar .env y añadir tu OPENAI_API_KEY
# Usa tu editor favorito: nano, vim, VSCode, etc.
nano .env
```

Tu `.env` debe verse así:
```bash
OPENAI_API_KEY=sk-proj-...tu-key-real-aqui...
```

### 3️⃣ Ejecutar el Script de Inicio

```bash
# Linux/Mac
./start-workshop.sh

# Windows (PowerShell)
.\start-workshop.bat
```

**¡Listo!** Abre tu navegador en **http://localhost:8888**

---

## 🛠️ Comandos Manuales (Alternativa)

Si prefieres control manual:

### Build de la Imagen
```bash
docker-compose build
```

### Iniciar Servicios
```bash
# Todos los servicios (Jupyter + ChromaDB + Redis)
docker-compose up -d

# Solo Jupyter
docker-compose up -d jupyter
```

### Ver Logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo Jupyter
docker-compose logs -f jupyter
```

### Detener Servicios
```bash
docker-compose down
```

### Reiniciar Servicios
```bash
docker-compose restart
```

### Acceder al Shell del Contenedor
```bash
docker-compose exec jupyter bash
```

---

## 🌐 Servicios Disponibles

Una vez iniciado, tienes acceso a:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Jupyter Lab** | http://localhost:8888 | Notebooks del workshop |
| **Streamlit** | http://localhost:8501 | Apps de demostración |
| **FastAPI** | http://localhost:8000 | API REST |
| **Gradio** | http://localhost:7860 | Interfaces ML |
| **ChromaDB** | http://localhost:8001 | Vector database server |
| **Redis** | localhost:6379 | Cache |

---

## 🔧 Configuración Avanzada

### Modificar Puertos

Edita `docker-compose.yml`:

```yaml
ports:
  - "9999:8888"  # Cambiar puerto de Jupyter a 9999
```

### Añadir Variables de Entorno

Edita `.env`:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
COHERE_API_KEY=...
```

### Usar GPU (NVIDIA)

Edita `docker-compose.yml`:

```yaml
services:
  jupyter:
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

---

## 📊 Volúmenes de Datos

Los siguientes directorios están montados en el contenedor:

```
./notebooks → /workspace/notebooks  (Tus notebooks)
./data      → /workspace/data       (Datos del workshop)
./src       → /workspace/src        (Código fuente)
./solutions → /workspace/solutions  (Soluciones)
```

**Tus cambios se guardan automáticamente** en tu máquina local.

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Docker daemon"

**Solución**: Asegúrate de que Docker Desktop esté corriendo.

```bash
# Linux
sudo systemctl start docker

# Mac/Windows
# Abre Docker Desktop manualmente
```

### Error: "Port already in use"

**Solución**: Otro servicio está usando el puerto 8888.

```bash
# Detener servicios conflictivos
docker-compose down

# O cambiar puerto en docker-compose.yml
```

### JupyterLab no carga

**Solución**: Espera 10-15 segundos después de iniciar.

```bash
# Ver si hay errores
docker-compose logs jupyter
```

### Problemas con permisos (Linux)

**Solución**: Añade tu usuario al grupo docker.

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Reinstalar desde cero

```bash
# Detener y eliminar todo
docker-compose down -v

# Eliminar imágenes
docker rmi rag-workshop-2025-jupyter

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

---

## 🧹 Limpieza

### Detener sin eliminar datos
```bash
docker-compose down
```

### Eliminar todo (contenedores + volúmenes)
```bash
docker-compose down -v
```

### Eliminar imágenes Docker
```bash
docker rmi rag-workshop-2025-jupyter chromadb/chroma redis:7-alpine
```

---

## 💡 Tips y Mejores Prácticas

### 1. **Guardar tu trabajo frecuentemente**
Los notebooks se guardan automáticamente, pero haz commits en git:

```bash
git add notebooks/
git commit -m "Progreso del workshop"
```

### 2. **Usar JupyterLab Extensions**
Instala extensiones útiles:

```bash
docker-compose exec jupyter bash
pip install jupyterlab-git jupyterlab-lsp
```

### 3. **Backup de ChromaDB**
Los datos de ChromaDB están en un volumen Docker:

```bash
# Ver volúmenes
docker volume ls

# Backup
docker run --rm -v rag-workshop-2025_chromadb-data:/data -v $(pwd):/backup ubuntu tar czf /backup/chromadb-backup.tar.gz /data
```

### 4. **Optimizar uso de memoria**

Si Docker usa mucha RAM:

- **Docker Desktop** → Settings → Resources → Memory (ajustar a 4-6 GB)

---

## 🆘 Soporte

Si tienes problemas:

1. **Revisa los logs**: `docker-compose logs -f`
2. **Consulta este documento**: Busca tu error en Troubleshooting
3. **Pregunta al instructor** durante el workshop

---

## 📚 Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/)

---

**🎓 RAG Workshop 2025** - Setup con Docker para máxima estabilidad
