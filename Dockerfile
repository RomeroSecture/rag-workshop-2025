# ============================================
# RAG Workshop 2025 - Dockerfile
# Python 3.11 - Ambiente Completo
# ============================================

FROM python:3.11-slim

# Metadata
LABEL maintainer="RAG Workshop 2025"
LABEL description="Ambiente completo para RAG Workshop con Jupyter, LangChain y LlamaIndex"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd -m -s /bin/bash workshop && \
    mkdir -p /workspace && \
    chown -R workshop:workshop /workspace

# Cambiar a usuario workshop
USER workshop
WORKDIR /workspace

# Configurar PATH para instalar paquetes localmente
ENV PATH="/home/workshop/.local/bin:${PATH}"

# Copiar requirements.txt
COPY --chown=workshop:workshop requirements.txt .

# Instalar dependencias Python
RUN pip install --user --upgrade pip && \
    pip install --user -r requirements.txt

# Copiar todo el proyecto
COPY --chown=workshop:workshop . .

# Exponer puertos
# 8888: JupyterLab
# 8501: Streamlit
# 8000: FastAPI
# 7860: Gradio
EXPOSE 8888 8501 8000 7860

# Comando por defecto: JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
