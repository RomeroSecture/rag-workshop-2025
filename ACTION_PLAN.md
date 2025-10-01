# 🎯 Plan de Acción - Preparar Workshop para GitHub

**Estado actual**: Estás en rama `solutions` con cambios sin commitear
**Objetivo**: Tener `main` listo para participantes y `solutions` para ti

---

## 📊 Estado Actual del Repo

### ✅ Lo que YA tienes (BUENO):

```bash
✅ Rama solutions existe
✅ Rama main existe
✅ Ambas ramas están en GitHub
✅ .devcontainer/ configurado
✅ Todos los notebooks listos
✅ Soluciones completas del Módulo 2
✅ Guías de instructor para M3-M5
✅ Documentación completa creada HOY
```

### 📝 Archivos Nuevos Creados HOY (sin commitear):

```
✅ SECURITY_API_KEYS.md              (seguridad API keys)
✅ BRANCH_STRUCTURE.md               (esta guía)
✅ INSTRUCTOR_CHECKLIST.md           (checklist día del workshop)
✅ QUICK_START_GUIDE.md              (guía 5 min para participantes)
✅ README_GITHUB_CODESPACES.md       (guía técnica Codespaces)
✅ SETUP_VERIFICATION.md             (setup local alternativo)
✅ WORKSHOP_READY_CHECKLIST.md       (estado de completitud)
✅ scripts/verify_setup.py           (script de verificación)
✅ solutions/nivel_2_workshop/       (4 soluciones nuevas + README)
✅ solutions/guias_instructor/       (movidas desde nivel_2_workshop)
✅ .env.example                      (actualizado con mejores comentarios)
```

---

## 🚀 PLAN DE ACCIÓN (Paso a Paso)

### PASO 1: Commit en `solutions` (5 minutos)

**Estás aquí ahora**. Commitea todo lo nuevo:

```bash
# Ya estás en solutions
git status

# Añadir TODO
git add .

# Commit con mensaje descriptivo
git commit -m "✅ Workshop completo: Soluciones M2 + Guías + Documentación

- Añadidas 7 soluciones completas Módulo 2
- Guías de instructor para M3-M5
- Documentación de seguridad API keys
- Scripts de verificación automatizados
- Guías de Codespaces y setup
- 22 archivos nuevos en total

Estado: 95% completo - LISTO para workshop"

# Push a GitHub
git push origin solutions
```

---

### PASO 2: Limpiar `main` para Participantes (10 minutos)

**Objetivo**: `main` debe tener SOLO lo necesario para participantes (sin soluciones).

```bash
# Cambiar a main
git checkout main

# Ver qué tiene actualmente
ls -la

# 1. VERIFICAR: ¿Existe carpeta solutions/ en main?
ls solutions/

# Si existe y tiene contenido → BORRARLA
git rm -rf solutions/
git commit -m "Remove solutions from main (participant branch)"
git push origin main

# 2. Sincronizar archivos buenos desde solutions
git checkout solutions -- notebooks/
git checkout solutions -- src/
git checkout solutions -- data/
git checkout solutions -- scripts/
git checkout solutions -- .devcontainer/
git checkout solutions -- requirements.txt
git checkout solutions -- .env.example
git checkout solutions -- .gitignore

# 3. Sincronizar documentación para participantes
git checkout solutions -- README.md
git checkout solutions -- QUICK_START_GUIDE.md
git checkout solutions -- SECURITY_API_KEYS.md

# 4. Commit y push
git add .
git commit -m "Sync participant files from solutions

- Notebooks actualizados
- Scripts de verificación
- Configuración de Codespaces
- Documentación de seguridad
- Guías de inicio rápido

NO incluye soluciones (solo en rama solutions)"

git push origin main
```

---

### PASO 3: Verificar Separación de Ramas (5 minutos)

```bash
# En main - NO debe tener soluciones
git checkout main
ls solutions/                  # Debe fallar o estar vacío
ls INSTRUCTOR_CHECKLIST.md     # No debe existir
ls README_GITHUB_CODESPACES.md # No debe existir

# En solutions - DEBE tener todo
git checkout solutions
ls solutions/nivel_2_workshop/  # ✅ 8 archivos (7 .py + 1 .md)
ls solutions/guias_instructor/  # ✅ 3 archivos .md
ls INSTRUCTOR_CHECKLIST.md      # ✅ Existe
ls README_GITHUB_CODESPACES.md  # ✅ Existe
```

**Si pasa las verificaciones** → ✅ LISTO

---

### PASO 4: Configurar GitHub (5 minutos)

```bash
# 1. Ve a tu repo en GitHub:
#    https://github.com/[TU-USUARIO]/rag-workshop-2025

# 2. Verificar Settings:
Settings → General
  ✅ Default branch: main
  ✅ Allow merge commits
  ✅ Allow squash merging

Settings → Branches
  ✅ main es la default branch

Settings → Codespaces (opcional)
  ✅ Enable Codespaces: ON

# 3. Verificar ramas en GitHub:
Code → Branches
  ✅ main (default)
  ✅ solutions (existe pero no default)

# 4. Hacer repo público (si quieres):
Settings → General → Change visibility
  → Make public
```

---

### PASO 5: Probar Codespaces COMPLETO (15 minutos)

**IMPORTANTE**: Hazlo 1 semana antes del workshop.

```bash
# 1. Ir al repo en GitHub
#    https://github.com/[TU-USUARIO]/rag-workshop-2025

# 2. Code → Codespaces → Create codespace on main
#    (Asegúrate de que sea en MAIN, no solutions)

# 3. Esperar 2-3 minutos mientras instala

# 4. Cuando aparezca el terminal, configurar API key:
cp .env.example .env
nano .env
# Pegar tu API key de OpenAI (la que me compartiste)
# Guardar: Ctrl+O, Enter, Ctrl+X

# 5. Verificar instalación:
python scripts/verify_setup.py
# Debe pasar TODAS las verificaciones

# 6. Probar notebooks:
# - Abrir: notebooks/00_inicio.ipynb
# - Select Kernel → Python 3.11
# - Ejecutar todas las celdas (Run All)

# 7. Si TODO funciona sin errores:
#    ✅ ¡LISTO PARA EL WORKSHOP!

# 8. Borrar este Codespace de prueba:
#    https://github.com/codespaces
#    → Delete
```

---

## 🔒 Manejo de tu API Key (IMPORTANTE)

### ⚠️ La API Key que me compartiste:

```
sk-proj-UXJD0g9vwHyzIdcca9GX3OYE5auGTm6cYBekCqs8xz...
```

### Opciones para el Workshop:

**OPCIÓN 1: Cada participante usa su propia key** (RECOMENDADO)
- Más seguro
- Sin límites de rate
- Les pides que traigan $5 USD en créditos

**OPCIÓN 2: Compartir tu key durante el workshop**
- Úsala SOLO como backup
- Compártela verbalmente (NO en pantalla)
- **REVÓCALA inmediatamente después del workshop**
- Crear nueva para tu uso personal

**NUNCA**:
- ❌ Commitear la key a Git
- ❌ Ponerla en archivos de código
- ❌ Mostrarla en pantalla proyectada
- ❌ Compartirla en Slack/chat que quede grabado

### Configurar Límites de Uso (Protección):

```
1. Ve a: https://platform.openai.com/account/limits
2. Monthly budget: $50 USD (para 20 personas)
3. Notification email: Tu email
4. Hard limit: ON (se detiene al llegar al límite)
```

---

## 📧 Email a Participantes (3 días antes)

```
Asunto: Workshop RAG 2025 - Preparación (5 minutos)

Hola equipo,

¡El workshop es en 3 días! 🚀

📋 PREPARA ESTO (toma 5 minutos):

1️⃣ Cuenta de GitHub (gratis)
   https://github.com/signup

2️⃣ API Key de OpenAI (recomendado: $5 USD)
   - Crear cuenta: https://platform.openai.com/signup
   - Añadir créditos: Settings → Billing
   - Crear API key: API Keys → Create new
   - GUARDAR la key (empieza con "sk-proj-")

   💡 El workshop gasta ~$2 USD por persona
   💡 Si no puedes, compartiré una key temporal

3️⃣ Navegador actualizado
   Chrome, Firefox, Safari o Edge

🚀 TODO el workshop es EN LA NUBE
NO necesitas instalar Python, Jupyter ni nada.

📱 PRUEBA AHORA (opcional):
1. https://github.com/[TU-USUARIO]/rag-workshop-2025
2. Clic en badge azul "Open in GitHub Codespaces"
3. Esperar 2-3 minutos
4. Configurar tu API key en .env
5. Ejecutar: python scripts/verify_setup.py

Si ves "✅ TODO LISTO" → ¡Perfecto!

¿Problemas? Escríbeme: aromero@secture.com

¡Nos vemos el [FECHA y HORA]!

Saludos,
[Tu nombre]
```

---

## ✅ Checklist Final (Antes del Workshop)

### **1 Semana Antes**:
- [ ] Push completo de `solutions` a GitHub
- [ ] `main` limpio (sin soluciones)
- [ ] Codespace de prueba funciona 100%
- [ ] Todos los notebooks corren sin errores
- [ ] API key con límites configurados
- [ ] Email enviado a participantes

### **3 Días Antes**:
- [ ] Confirmar asistencia
- [ ] Recordar crear GitHub account + API key
- [ ] Enviar link del repo nuevamente
- [ ] Confirmar venue e internet

### **1 Día Antes**:
- [ ] Revisar slides/presentación
- [ ] Imprimir INSTRUCTOR_CHECKLIST.md
- [ ] Preparar hotspot móvil (backup)
- [ ] Cargar laptop completamente
- [ ] Crear chat/Slack del workshop

### **Día del Workshop**:
- [ ] Llegar 30 min antes
- [ ] Probar proyector/pantalla
- [ ] Probar internet del venue
- [ ] Tener tu Codespace abierto
- [ ] Rama `solutions` en otra pestaña (para consultar)
- [ ] INSTRUCTOR_CHECKLIST.md impreso

---

## 🎯 Resumen Visual de Estado

```
┌─────────────────────────────────────────┐
│  RAMA: main (para participantes)        │
├─────────────────────────────────────────┤
│  Estado: LISTO después del PASO 2       │
│                                         │
│  ✅ Notebooks (sin soluciones)          │
│  ✅ Código base                          │
│  ✅ Scripts de verificación              │
│  ✅ Configuración Codespaces             │
│  ✅ Guías de inicio                      │
│  ❌ Sin carpeta solutions/               │
│  ❌ Sin archivos de instructor           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  RAMA: solutions (para ti)              │
├─────────────────────────────────────────┤
│  Estado: COMPLETO (después del PASO 1)  │
│                                         │
│  ✅ Todo de main                         │
│  ✅ + 7 soluciones Módulo 2             │
│  ✅ + 3 guías instructor                 │
│  ✅ + 7 documentos técnicos              │
│  ✅ + Checklists                         │
│                                         │
│  Total: 22 archivos nuevos              │
└─────────────────────────────────────────┘
```

---

## 🆘 Si Algo Sale Mal

### Problema: "No puedo crear Codespace"
```
Solución:
1. Verificar que repo es público o participante tiene acceso
2. Verificar Settings → Codespaces → Enable
3. Intentar desde otro navegador
4. Plan B: Setup local (15 min extra)
```

### Problema: "API Key no funciona"
```
Solución:
1. Verificar que empieza con "sk-proj-" o "sk-"
2. Verificar que tiene créditos en OpenAI
3. Crear nueva API key
4. Plan B: Compartir tu key temporalmente
```

### Problema: "Jupyter no abre notebooks"
```
Solución:
1. Ctrl+Shift+P → "Reload Window"
2. Select Kernel → Python 3.11
3. Si persiste: Rebuild Container
```

---

## 📞 Soporte

**Antes del workshop**:
- Email: aromero@secture.com
- GitHub Issues del repo

**Durante el workshop**:
- Chat/Slack en vivo
- Instructores asistentes

---

## 🎉 ¡ESTÁS CASI LISTO!

**Sigue los 5 pasos en orden** y estarás 100% preparado.

**Tiempo total estimado**: 40 minutos
- PASO 1: 5 min (commit solutions)
- PASO 2: 10 min (limpiar main)
- PASO 3: 5 min (verificar)
- PASO 4: 5 min (config GitHub)
- PASO 5: 15 min (probar Codespace)

**¿Dudas?** Pregúntame lo que necesites 🙋

---

**Última actualización**: 2025-10-01
**Siguiente paso**: PASO 1 - Commit en solutions
