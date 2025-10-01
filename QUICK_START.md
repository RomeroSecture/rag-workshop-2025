# ⚡ Quick Start - RAG Workshop 2025

Guía rápida para empezar en **menos de 5 minutos**.

---

## 🚀 Para Alumnos del Workshop

### ✅ Opción 1: GitHub Codespaces (RECOMENDADO)

**Sin instalación, todo en el navegador**

1. **Haz fork de este repositorio**
   - Click en el botón "Fork" arriba a la derecha
   - Esto crea tu propia copia del proyecto

2. **Crea tu Codespace**
   - En TU fork, click en el botón verde **"Code"**
   - Pestaña **"Codespaces"**
   - Click **"Create codespace on main"**

3. **Espera 3-5 minutos** ⏳
   - Se está instalando todo automáticamente
   - Verás mensajes de progreso en el terminal

4. **Configura tu API Key**
   ```bash
   # Abre el archivo .env
   # Reemplaza: OPENAI_API_KEY=sk-YOUR-API-KEY-HERE
   # Con tu key real: OPENAI_API_KEY=sk-proj-...
   ```

5. **Verifica que todo funciona**
   - Abre: `notebooks/00_inicio.ipynb`
   - Ejecuta las celdas con Shift+Enter
   - Si ves ✅ en todas, ¡estás listo!

---

### 📱 Opción 2: Google Colab (Backup)

Si tienes problemas con Codespaces:

1. Ve a [colab.research.google.com](https://colab.research.google.com)
2. File → Open Notebook → GitHub
3. Pega: `https://github.com/[TU-USUARIO]/rag-workshop-2025`
4. Selecciona `notebooks/00_inicio.ipynb`

**⚠️ Nota**: Necesitarás clonar el repo en cada sesión

---

### 💻 Opción 3: Local (Avanzado)

Si prefieres trabajar en tu máquina:

```bash
# 1. Clonar
git clone https://github.com/[TU-USUARIO]/rag-workshop-2025
cd rag-workshop-2025

# 2. Ambiente virtual (Python 3.11+)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias (~5 minutos)
pip install -r requirements.txt

# 4. Configurar API key
cp .env.example .env
# Editar .env con tu editor

# 5. Verificar instalación
python src/health_check.py

# 6. Lanzar Jupyter
jupyter lab
```

---

## 🔑 Obtener tu API Key de OpenAI

1. Ve a: https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Click en **"Create new secret key"**
4. Copia la key (empieza con `sk-proj-...`)
5. **¡Guárdala!** No podrás verla de nuevo

### 💰 Añadir Créditos

1. Ve a: https://platform.openai.com/account/billing
2. Add payment method
3. Añade mínimo **$5 USD** (suficiente para el workshop)
4. Espera 5-10 minutos para que se active

---

## 🐛 Troubleshooting Rápido

### "API Key inválida"
- Verifica que copiaste la key completa
- No uses comillas en el archivo `.env`
- Recarga: `load_dotenv(override=True)`

### "Insufficient quota"
- No tienes créditos suficientes
- Añade créditos en billing
- Espera 10 minutos

### "Module not found"
- Reinstala: `pip install -r requirements.txt --upgrade`
- Reinicia el kernel del notebook

### Codespace no carga
- Refresca el navegador (Ctrl+F5)
- Usa Chrome o Firefox
- Elimina y recrea el codespace

**📚 Más soluciones**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## ✅ Checklist Pre-Workshop

Antes del día del workshop:

- [ ] Fork del repositorio hecho
- [ ] Codespace creado y probado
- [ ] API Key de OpenAI obtenida
- [ ] Créditos añadidos ($5 mínimo)
- [ ] Notebook `00_inicio.ipynb` ejecutado sin errores
- [ ] Todas las celdas muestran ✅

---

## 📞 Ayuda

### Durante el Workshop
- 💬 **Slack**: #rag-workshop-2025
- 🙋 **Levanta la mano** (virtual o presencial)

### Fuera del Workshop
- 📧 **Email**: aromero@secture.com
- 📚 **Docs**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 🎯 Primer Paso

Una vez todo listo:

👉 **Abre** [`notebooks/00_inicio.ipynb`](notebooks/00_inicio.ipynb)

**¡Nos vemos en el workshop!** 🚀

---

*Última actualización: Octubre 2025*
