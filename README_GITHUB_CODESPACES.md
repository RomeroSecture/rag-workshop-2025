# ☁️ GitHub Codespaces - Setup Completo para Instructores

## 📋 Resumen Ejecutivo

**✅ TU WORKSHOP YA ESTÁ CONFIGURADO PARA CODESPACES**

Los participantes NO necesitarán:
- ❌ Instalar Python
- ❌ Instalar dependencias
- ❌ Configurar Jupyter
- ❌ Descargar nada

**Todo funciona 100% en el navegador** mediante GitHub Codespaces.

---

## 🎯 Cómo Funciona

### Para Participantes (Su Experiencia)

```
1. Abren link del repo
2. Clic en "Create codespace"
3. Esperan 2-3 minutos (café ☕)
4. Configuran API key
5. ¡A trabajar!
```

**Detrás de escenas**, Codespaces:
- ✅ Crea contenedor Docker con Python 3.11
- ✅ Instala TODAS las dependencias (requirements.txt)
- ✅ Configura VS Code con extensiones
- ✅ Prepara Jupyter Lab
- ✅ Ejecuta script de setup automático

---

## 🔧 Archivos de Configuración (Ya están listos)

### 1. `.devcontainer/devcontainer.json`

**YA EXISTE** en tu repo. Esto es lo que hace:

```json
{
  "name": "RAG Workshop 2025",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  // Instala Python 3.11 + Jupyter automáticamente
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "installJupyterlab": true
    }
  },

  // Extensiones de VS Code pre-instaladas
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",           // Python support
        "ms-toolsai.jupyter",          // Jupyter notebooks
        "github.copilot"               // Copilot (si tienen)
      ]
    }
  },

  // Puertos expuestos (FastAPI, Streamlit, Jupyter)
  "forwardPorts": [8501, 8000, 8888],

  // Script que se ejecuta después de crear el contenedor
  "postCreateCommand": "bash .devcontainer/postCreateCommand.sh"
}
```

### 2. `.devcontainer/postCreateCommand.sh`

**YA EXISTE** en tu repo. Esto es lo que hace:

```bash
#!/bin/bash
# Se ejecuta automáticamente al crear el Codespace

# 1. Actualiza pip
pip install --upgrade pip

# 2. Instala TODAS las dependencias
pip install -r requirements.txt

# 3. Crea directorios necesarios
mkdir -p data/processed data/vectordb data/cache

# 4. Copia template de .env
cp .env.example .env

# 5. Configura Jupyter
python -m ipykernel install --user

# 6. Mensaje de bienvenida
echo "🚀 RAG Workshop Environment Ready!"
```

### 3. `requirements.txt`

**YA EXISTE** con TODAS las dependencias:
- OpenAI, Anthropic, Cohere
- LangChain + LangGraph
- LlamaIndex
- ChromaDB, Faiss, Pinecone, Qdrant
- FastAPI, Streamlit, Gradio
- Pandas, NumPy, Matplotlib
- PyPDF2, python-docx
- Y 40+ paquetes más

**Total**: ~2GB de dependencias instaladas automáticamente.

---

## 📊 Costo y Límites de Codespaces

### Para Participantes (Cuenta Personal GitHub)

**GRATIS**:
- ✅ 120 horas/mes de "core" (2 cores, 4GB RAM)
- ✅ 60 horas/mes de "standard" (4 cores, 8GB RAM)
- ✅ 15GB de almacenamiento

**Para el workshop (8 horas)**:
- Usa 8 horas del límite gratuito
- **100% GRATIS** si es su primer codespace del mes

### Para Ti (Instructor)

Si tienes **GitHub Pro** ($4/mes):
- 180 horas/mes gratis

Si usas cuenta **Organizacional**:
- Configurar billing en Settings → Billing → Codespaces
- Costo: ~$0.18/hora por "standard" codespace
- 1 participante × 8 horas = ~$1.44 USD

**RECOMENDACIÓN**: Que cada participante use su propia cuenta (gratis para ellos).

---

## 🚀 Pasos para Preparar el Repo (Antes del Workshop)

### 1. Verifica que los archivos de configuración existen

```bash
cd /Users/antonioromero/Desktop/Proyectos/rag-workshop-2025

# Deben existir:
ls -la .devcontainer/devcontainer.json
ls -la .devcontainer/postCreateCommand.sh
ls -la requirements.txt
ls -la .env.example
```

✅ **Todos existen** en tu repo actual.

### 2. Haz push a GitHub

```bash
# Asegúrate de estar en la rama main (sin soluciones)
git checkout main

# Verificar que NO tienes soluciones en main
ls solutions/  # Debe estar vacío o no existir

# Commit y push
git add .
git commit -m "Workshop ready for Codespaces"
git push origin main
```

### 3. Habilita Codespaces en el Repo

```
1. Ve a tu repo en GitHub
2. Settings → Codespaces
3. Marcar: "Enable Codespaces for this repository"
4. (Ya debería estar habilitado por defecto)
```

### 4. Haz el Repo Público o Invita a Participantes

**Opción A: Repo Público** (Más fácil)
```
Settings → General → Change visibility → Make public
```

**Opción B: Repo Privado + Invitar** (Más control)
```
Settings → Collaborators → Add people
(Añadir email de cada participante)
```

### 5. Agrega Badge "Open in Codespaces" al README

En tu `README.md`, añade al inicio:

```markdown
# RAG Workshop 2025

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/[TU-USUARIO]/rag-workshop-2025?quickstart=1)

## 🚀 Inicio Rápido

Haz clic en el badge de arriba para abrir este workshop en GitHub Codespaces (todo en la nube).
```

Reemplaza `[TU-USUARIO]` con tu username de GitHub.

---

## 🧪 Prueba TÚ MISMO el Codespace

**IMPORTANTE**: Hazlo 1 semana antes del workshop.

### 1. Crea tu Codespace

```
1. Ve a tu repo en GitHub
2. Botón verde "Code"
3. Pestaña "Codespaces"
4. "Create codespace on main"
```

### 2. Espera la Instalación (2-3 minutos)

Verás en el terminal:
```
🔧 Configurando ambiente RAG Workshop...
📦 Instalando dependencias...
[... muchas líneas ...]
✅ Setup completado
🚀 RAG Workshop Environment Ready!
```

### 3. Configura API Key

```bash
cp .env.example .env
nano .env
# Edita OPENAI_API_KEY
```

### 4. Verifica Instalación

```bash
python scripts/verify_setup.py
```

Debe pasar TODAS las verificaciones.

### 5. Prueba un Notebook

```
1. Abrir: notebooks/00_inicio.ipynb
2. Select Kernel → Python 3.11
3. Ejecutar todas las celdas (Shift + Enter)
```

**Todo debe correr sin errores.**

---

## 📧 Email Template para Participantes

Envía esto 3 días antes del workshop:

```
Asunto: Workshop RAG 2025 - Acceso a Codespaces (TODO EN LA NUBE)

Hola equipo,

¡El workshop es en 3 días! 🎉

EXCELENTE NOTICIA: Todo el workshop es 100% en la nube con GitHub Codespaces.
NO necesitan instalar NADA en su computadora.

🔗 LINK DEL WORKSHOP:
https://github.com/[TU-USUARIO]/rag-workshop-2025

📋 LO ÚNICO QUE NECESITAS:

1. Cuenta de GitHub (gratis)
   → Si no tienes: https://github.com/signup

2. API Key de OpenAI ($5 USD de créditos)
   → Crear aquí: https://platform.openai.com/api-keys
   → Añadir créditos: Settings → Billing
   → El workshop consume ~$2-3 USD

3. Navegador actualizado (Chrome/Firefox/Safari/Edge)

✅ OPCIONAL: Prueba el ambiente AHORA

1. Abre el link de arriba
2. Clic en el badge azul "Open in GitHub Codespaces"
3. Espera 2-3 minutos
4. Configura tu API key en .env
5. Ejecuta: python scripts/verify_setup.py

Si todo sale bien, verás: ✅ TODO LISTO PARA EL WORKSHOP!

¿Problemas? Escríbeme a aromero@secture.com

¡Nos vemos el [FECHA]!

Saludos,
[Tu nombre]
```

---

## 🎬 Día del Workshop - Setup Guiado (15 minutos)

### Proyecta en pantalla y guía paso a paso:

```
👨‍🏫 INSTRUCTOR: "Buenos días a todos. Vamos a configurar
                 el ambiente juntos en 10 minutos."

1️⃣ "Todos abren GitHub.com y hacen login"
   (Esperar a que todos estén logueados)

2️⃣ "Abran este link que comparto en el chat:"
   https://github.com/[TU-USUARIO]/rag-workshop-2025

3️⃣ "Hagan clic en el badge azul 'Open in GitHub Codespaces'"
   O: Code → Codespaces → Create codespace

4️⃣ "ESPERAMOS JUNTOS 2-3 minutos"
   (Momento perfecto para presentaciones rápidas)
   (Pon música de espera si quieres 🎵)

5️⃣ "Cuando vean: 🚀 RAG Workshop Environment Ready!"
   (Pedir que levanten la mano cuando lo vean)
   (Aplaudir cuando todos estén listos 👏)

6️⃣ "Ahora configuramos API key"
   (Mostrar EN PANTALLA cómo hacerlo)
   - cp .env.example .env
   - Click en .env en explorador
   - Pegar su API key
   - Guardar (Cmd+S / Ctrl+S)

7️⃣ "Verificamos instalación"
   python scripts/verify_setup.py
   (Pedir que levanten mano si ven ✅ TODO LISTO)

8️⃣ "Abrimos primer notebook"
   notebooks/00_inicio.ipynb
   (Ejecutar primera celda juntos)

🎉 "¡LISTOS PARA EMPEZAR EL WORKSHOP!"
```

---

## ⚠️ Troubleshooting Común

### "Codespace no inicia"

```bash
# Solución 1: Reload
Ctrl+Shift+P → Developer: Reload Window

# Solución 2: Rebuild
Ctrl+Shift+P → Codespaces: Rebuild Container

# Solución 3: Nuevo Codespace
Delete el actual y crear uno nuevo
```

### "Jupyter no encuentra kernel"

```bash
# En terminal del Codespace:
python -m ipykernel install --user --name rag-env
# Luego recargar VSCode
```

### "Errores al instalar dependencias"

```bash
# Reinstalar todo
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### "Límite de Codespaces alcanzado"

```
Error: "You've reached your limit of 2 active codespaces"

Solución:
1. Ve a: https://github.com/codespaces
2. Borra un Codespace viejo
3. Crea uno nuevo
```

---

## 💰 Optimización de Costos

### Para Participantes (Gratis)

- Usar cuenta personal de GitHub (60 horas gratis/mes)
- Cerrar Codespace después del workshop (Settings → Stop)
- Se puede reabrir después (persiste 30 días)

### Para Organizaciones (Pagar por horas)

```
Configurar billing:
Settings → Billing → Codespaces → Add payment method

Costo por participante (8 horas):
- Machine type "standard" (4 cores, 8GB): $0.18/hora
- Total: 8h × $0.18 = $1.44 USD por persona

Para 20 participantes: ~$29 USD total
```

**RECOMENDACIÓN**: Que cada uno use su cuenta personal (gratis).

---

## 📊 Métricas y Monitoreo

### Durante el Workshop

Puedes ver cuántos Codespaces están activos:

```
1. Ve a tu repo
2. Insights → Traffic → Codespaces
3. Ver número de instancias activas
```

### Después del Workshop

```
Settings → Codespaces → Usage
→ Ver cuántas horas se usaron
→ Ver costos (si hay)
```

---

## ✅ Checklist Final

**1 Semana Antes**:
- [ ] Archivos de configuración en el repo
- [ ] Push a GitHub
- [ ] Codespaces habilitado
- [ ] Badge añadido al README
- [ ] Probar creando TU codespace
- [ ] Verificar que todos los notebooks corren

**3 Días Antes**:
- [ ] Email a participantes con instrucciones
- [ ] Compartir link del repo
- [ ] Recordar: Crear cuenta GitHub + API key OpenAI

**Día del Workshop**:
- [ ] Tu Codespace abierto y listo
- [ ] Link del repo en el proyector
- [ ] 15 min para setup guiado
- [ ] Verificar que todos tienen ✅ TODO LISTO

---

## 🆘 Soporte

**Si algo NO funciona**:

1. **Plan A**: Troubleshooting en vivo (5 min max)
2. **Plan B**: Trabajar de a pares con alguien que sí le funciona
3. **Plan C**: Setup local en su Mac (15 min extra)

**Link a setup local**: `SETUP_VERIFICATION.md` (ya existe en tu repo)

---

## 🎉 Ventajas de Codespaces para Workshop

✅ **Todos tienen ambiente idéntico** (no más "en mi máquina funciona")
✅ **Setup automático** (no perder 30 min instalando)
✅ **Funciona en cualquier computadora** (Mac, Windows, Linux, Chromebook)
✅ **No consume recursos locales** (laptops no se recalientan)
✅ **Fácil de resetear** si algo se rompe
✅ **Accesible desde casa** después del workshop
✅ **Gratis** para participantes (con cuenta personal)

---

## 📚 Recursos Adicionales

- [Docs de GitHub Codespaces](https://docs.github.com/en/codespaces)
- [Guía de Dev Containers](https://containers.dev/)
- [VSCode en Codespaces](https://code.visualstudio.com/docs/remote/codespaces)

---

**¡Tu workshop está 100% listo para Codespaces!** 🚀

**Última actualización**: 2025-10-01
**Autor**: Antonio Romero (aromero@secture.com)
