# 🚀 RAG Workshop 2025 - De Cero a Producción en 8 Horas

[![GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://github.com/codespaces)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Descripción

Workshop intensivo de 8 horas para dominar Retrieval-Augmented Generation (RAG) desde los fundamentos hasta la implementación en producción. 

### 🎯 Lo que aprenderás:
- ✅ Fundamentos de RAG y arquitecturas
- ✅ Implementación desde cero
- ✅ Optimización de rendimiento (75% reducción de latencia)
- ✅ Frameworks modernos (LangChain, LlamaIndex)
- ✅ Despliegue en producción
- ✅ Mejores prácticas y patrones

## 🚀 Quick Start (Para Alumnos)

> **📖 Guías detalladas**: [DOCKER_SETUP.md](DOCKER_SETUP.md) | [QUICK_START.md](QUICK_START.md)

### Opción 1: Docker 🐳 (⭐ RECOMENDADO - Máxima Estabilidad)

**Ambiente 100% consistente, sin problemas de versiones**

```bash
# 1. Clonar repositorio
git clone https://github.com/[tu-usuario]/rag-workshop-2025.git
cd rag-workshop-2025

# 2. Configurar API key
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY

# 3. Iniciar con un comando
./start-workshop.sh  # Linux/Mac
# o start-workshop.bat en Windows

# 4. Abrir navegador en http://localhost:8888
```

📘 **Guía completa**: [DOCKER_SETUP.md](DOCKER_SETUP.md)

### Opción 2: GitHub Codespaces

1. **Fork este repositorio**
   - Click en el botón "Fork" arriba a la derecha
   
2. **Crear tu Codespace**
   - En tu fork, click en el botón verde "Code"
   - Selecciona la pestaña "Codespaces"
   - Click en "Create codespace on main"
   
3. **Esperar 3-5 minutos** mientras se configura el ambiente automáticamente

4. **Configurar tu API Key**
   ```bash
   # En el terminal del Codespace
   cp .env.example .env
   # Editar .env y añadir tu OPENAI_API_KEY
   ```

5. **Abrir el primer notebook**
   - Navega a `notebooks/00_inicio.ipynb`
   - ¡Listo para empezar!

### Opción 3: Google Colab (Backup)

Si tienes problemas con Codespaces:

1. Ve a [Google Colab](https://colab.research.google.com)
2. File → Open Notebook → GitHub
3. Pega: `https://github.com/[tu-usuario]/rag-workshop-2025`
4. Selecciona el notebook deseado

### Opción 4: Instalación Local

**⚠️ Requisito**: Python 3.11 (recomendado para evitar conflictos de dependencias)

```bash
# Verificar versión de Python
python --version  # Debe ser Python 3.11.x

# Clonar el repositorio
git clone https://github.com/[tu-usuario]/rag-workshop-2025
cd rag-workshop-2025

# Crear ambiente virtual con Python 3.11
python3.11 -m venv venv  # o 'python -m venv venv' si ya tienes 3.11
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Editar .env con tu editor favorito

# Lanzar Jupyter
jupyter lab
```

**📘 Instalación de Python 3.11**: Ver [ENVIRONMENT.md](ENVIRONMENT.md) para instrucciones detalladas

## 📚 Estructura del Workshop

### Módulos

| Módulo | Tiempo | Contenido | Notebook |
|--------|--------|-----------|----------|
| **Apertura** | 08:00-08:15 | Setup y verificación | `00_inicio.ipynb` |
| **Módulo 1** | 08:15-09:30 | Fundamentos RAG | `01_fundamentos.ipynb` |
| **Módulo 2** | 09:45-11:15 | Arquitectura y Optimización | `02_arquitectura.ipynb` |
| **Módulo 3** | 12:00-13:30 | Frameworks Avanzados | `03_frameworks.ipynb` |
| **Módulo 4** | 13:45-15:00 | Producción y Escalado | `04_produccion.ipynb` |
| **Proyecto** | 15:00-15:45 | Tu propio sistema RAG | `05_proyecto_final.ipynb` |

### Estructura del Proyecto

```
rag-workshop-2025/
├── notebooks/          # Notebooks interactivos
├── src/               # Código modular
│   ├── shared_config.py
│   ├── module_1_basics.py
│   ├── module_2_optimized.py
│   ├── module_3_advanced.py
│   └── module_4_production.py
├── data/              # Documentos de ejemplo
├── tests/             # Tests unitarios
└── docs/              # Documentación adicional
```

## 🔧 Requisitos

### Software
- Python 3.11+
- Git
- Navegador web moderno

### API Keys Necesarias
- **OpenAI API Key** (Requerido) - [Obtener aquí](https://platform.openai.com/api-keys)
- Anthropic API Key (Opcional)
- Cohere API Key (Opcional)

### Costo Estimado
- ~$2-3 USD por persona para todo el workshop
- Recomendado: $5-10 de créditos para experimentar

## 💡 Tips para el Workshop

### Antes del Workshop
- [ ] Crear cuenta en GitHub
- [ ] Obtener API key de OpenAI
- [ ] Hacer fork del repositorio
- [ ] Probar que puedes crear un Codespace

### Durante el Workshop
- 🎯 Experimenta sin miedo - los errores son aprendizaje
- 💬 Pregunta todo - no hay preguntas tontas
- 📝 Toma notas de tus "aha moments"
- 🤝 Ayuda a tus compañeros
- 💡 Piensa en tu caso de uso real

### Atajos de Jupyter
- `Shift + Enter` - Ejecutar y avanzar
- `Ctrl + Enter` - Ejecutar sin avanzar
- `Tab` - Autocompletar
- `Shift + Tab` - Ver documentación

## 🐛 Troubleshooting

### Problema: "API Key no válida"
```python
# Verificar que tu .env tiene:
OPENAI_API_KEY=sk-...  # Tu key real aquí

# Recargar el ambiente:
from dotenv import load_dotenv
load_dotenv(override=True)
```

### Problema: "ModuleNotFoundError"
```bash
# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

### Problema: "Codespace no carga"
- Intenta refrescar el navegador
- Usa otro navegador (Chrome/Firefox recomendados)
- Como último recurso, usa Google Colab

## 📊 Métricas de Éxito

Al finalizar el workshop podrás:

| Métrica | Baseline | Tu Sistema |
|---------|----------|------------|
| Latencia | 2000ms | <500ms |
| Costo/query | $0.01 | <$0.004 |
| Accuracy | 70% | >90% |
| Queries/seg | 1 | >10 |

## 🤝 Soporte

### Durante el Workshop
- 💬 Slack: #rag-workshop-2025
- 🙋 Levanta la mano virtual
- 👥 Pregunta a tu buddy

### Después del Workshop
- 📧 Email: aromero@secture.com
- 📚 [Documentación extendida](docs/)
- 🎥 Grabación disponible en 48h

## 🎓 Certificación

Al completar el workshop recibirás:
- ✅ Certificado de participación
- ✅ Badge de LinkedIn
- ✅ Acceso al repositorio actualizado
- ✅ Invitación a la comunidad RAG

## 📚 Recursos Adicionales

### Documentación Oficial
- [OpenAI Documentation](https://platform.openai.com/docs)
- [LangChain Docs](https://python.langchain.com/)
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [ChromaDB Docs](https://docs.trychroma.com/)

### Lecturas Recomendadas
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [RAG Paper Original](https://arxiv.org/abs/2005.11401)
- [OpenAI Cookbook](https://cookbook.openai.com/)

### Comunidades
- [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA)
- [LangChain Discord](https://discord.gg/langchain)
- [OpenAI Community](https://community.openai.com/)

## 📈 Siguientes Pasos

Después del workshop:

1. **Semana 1**: Implementa RAG en un proyecto piloto
2. **Semana 2**: Optimiza basándote en métricas reales
3. **Semana 3**: Escala a producción
4. **Semana 4**: Comparte tu experiencia

## 🙏 Agradecimientos

- OpenAI por las APIs
- LangChain y LlamaIndex por los frameworks
- La comunidad open source
- ¡Y a ti por participar!

## 📄 Licencia

Este proyecto está bajo licencia MIT. Siéntete libre de usar el código en tus proyectos.

---

**¿Listo para empezar?** 🚀

👉 [Abre tu primer notebook](notebooks/00_inicio.ipynb) y comencemos el viaje RAG!

---

*Creado con ❤️ para la comunidad RAG*