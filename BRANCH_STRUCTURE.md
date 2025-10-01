# 🌳 Estructura de Ramas - Workshop RAG 2025

## 📋 Resumen Ejecutivo

**2 Ramas Principales**:
- **`main`**: Para PARTICIPANTES (pública, sin soluciones)
- **`solutions`**: Para INSTRUCTORES (privada, con todas las soluciones)

---

## 🌿 Rama `main` - Para Participantes

### ✅ QUÉ INCLUIR (Participantes necesitan esto)

```
main/
├── .devcontainer/           ✅ Configuración de Codespaces
│   ├── devcontainer.json
│   └── postCreateCommand.sh
│
├── notebooks/               ✅ Notebooks del workshop
│   ├── 00_inicio.ipynb
│   ├── 01_fundamentos.ipynb
│   ├── 02_arquitectura.ipynb
│   ├── 03_frameworks.ipynb
│   ├── 04_produccion.ipynb
│   └── 05_proyecto_final.ipynb
│
├── src/                     ✅ Código base del workshop
│   ├── shared_config.py
│   ├── module_1_basics.py
│   ├── module_2_optimized.py
│   ├── module_3_advanced.py
│   ├── module_4_production.py
│   └── utils.py
│
├── data/                    ✅ Datos de ejemplo
│   ├── company_handbook.pdf
│   ├── technical_docs.pdf
│   ├── faqs.json
│   └── support_tickets.csv
│
├── scripts/                 ✅ Scripts de utilidad
│   └── verify_setup.py      (verificación de instalación)
│
├── .env.example             ✅ Template de configuración
├── .gitignore               ✅ Protección de archivos sensibles
├── requirements.txt         ✅ Dependencias
│
├── README.md                ✅ Documentación principal
├── QUICK_START_GUIDE.md     ✅ Guía de inicio rápido
├── SETUP_VERIFICATION.md    ✅ Alternativa: setup local
├── SECURITY_API_KEYS.md     ✅ Guía de seguridad
│
└── WORKSHOP_READY_CHECKLIST.md  ⚠️ OPCIONAL (puede confundir)
```

### ❌ QUÉ NO INCLUIR (Mantener oculto)

```
❌ solutions/                  (carpeta completa)
❌ INSTRUCTOR_CHECKLIST.md     (checklist para instructores)
❌ README_GITHUB_CODESPACES.md (solo para instructor)
❌ BRANCH_STRUCTURE.md         (este archivo)
❌ .env                        (archivo con API keys reales)
❌ Cualquier archivo con soluciones completas
```

---

## 🔐 Rama `solutions` - Para Instructores

### ✅ TODO lo de `main` MÁS:

```
solutions/
├── (Todo lo de main)
│
├── solutions/               ✅ Soluciones completas
│   ├── README.md            (Guía de 3 niveles)
│   │
│   ├── nivel_1_basico/
│   │   └── 02_solucion_ejercicio1.py
│   │
│   ├── nivel_2_workshop/    ✅ COMPLETO
│   │   ├── README_SOLUCIONES.md
│   │   ├── 02_solucion_ejercicio1.py
│   │   ├── 02_solucion_ejercicio2.py
│   │   ├── 02_solucion_ejercicio3.py
│   │   ├── 02_solucion_ejercicio4_temperaturas.py
│   │   ├── 02_solucion_desafio_smart_chunking.py
│   │   ├── 02_solucion_desafio_metadata_indexing.py
│   │   └── 02_solucion_desafio_reranking.py
│   │
│   ├── nivel_3_produccion/
│   │   └── 02_solucion_ejercicio1.py
│   │
│   └── guias_instructor/    ✅ COMPLETO
│       ├── NOTEBOOK_03_frameworks_guia.md
│       ├── NOTEBOOK_04_produccion_guia.md
│       └── NOTEBOOK_05_proyecto_final_guia.md
│
├── INSTRUCTOR_CHECKLIST.md  ✅ Checklist día del workshop
├── README_GITHUB_CODESPACES.md  ✅ Guía técnica Codespaces
├── BRANCH_STRUCTURE.md      ✅ Este archivo
└── WORKSHOP_READY_CHECKLIST.md  ✅ Estado de completitud
```

---

## 🔄 Comandos Git para Mantener las Ramas

### Estado Actual (Verificar)

```bash
# Ver en qué rama estás
git branch

# Ver archivos en cada rama
git checkout main
ls -la solutions/  # No debe existir o estar vacío

git checkout solutions
ls -la solutions/  # Debe tener todas las soluciones
```

---

### Flujo de Trabajo Recomendado

#### 1. Trabajar en `solutions` (tu rama principal)

```bash
# Todos los cambios los haces aquí
git checkout solutions

# Hacer cambios...
git add .
git commit -m "Descripción del cambio"
git push origin solutions
```

#### 2. Sincronizar cambios generales a `main`

**Solo archivos que participantes necesitan**:

```bash
# Estando en solutions
git checkout solutions

# Copiar archivos específicos a main
git checkout main

# Merge selectivo (solo ciertos archivos)
git checkout solutions -- notebooks/
git checkout solutions -- src/
git checkout solutions -- data/
git checkout solutions -- scripts/
git checkout solutions -- .devcontainer/
git checkout solutions -- requirements.txt
git checkout solutions -- .env.example
git checkout solutions -- .gitignore
git checkout solutions -- README.md
git checkout solutions -- QUICK_START_GUIDE.md
git checkout solutions -- SETUP_VERIFICATION.md
git checkout solutions -- SECURITY_API_KEYS.md

# Commit en main
git add .
git commit -m "Sync participant files from solutions"
git push origin main

# Volver a solutions
git checkout solutions
```

---

### Script Automático de Sincronización

Crea este script para hacerlo más fácil:

```bash
#!/bin/bash
# sync_to_main.sh

echo "🔄 Sincronizando archivos de solutions a main..."

# Guardar rama actual
CURRENT_BRANCH=$(git branch --show-current)

# Asegurar que estamos en solutions
git checkout solutions

# Ir a main
git checkout main

# Archivos y carpetas para sincronizar
FILES=(
    "notebooks/"
    "src/"
    "data/"
    "scripts/"
    ".devcontainer/"
    "requirements.txt"
    ".env.example"
    ".gitignore"
    "README.md"
    "QUICK_START_GUIDE.md"
    "SETUP_VERIFICATION.md"
    "SECURITY_API_KEYS.md"
)

# Copiar cada archivo
for file in "${FILES[@]}"; do
    echo "  Copiando: $file"
    git checkout solutions -- "$file"
done

# Mostrar cambios
echo ""
echo "📋 Cambios a commitear:"
git status

# Pedir confirmación
read -p "¿Hacer commit y push? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    git commit -m "Sync from solutions: $(date +%Y-%m-%d)"
    git push origin main
    echo "✅ Sincronización completada"
else
    echo "⚠️  Cambios no commiteados"
fi

# Volver a rama original
git checkout "$CURRENT_BRANCH"
```

**Hacer ejecutable**:
```bash
chmod +x sync_to_main.sh
```

**Usar**:
```bash
./sync_to_main.sh
```

---

## 📊 Checklist de Archivos por Rama

### Para Verificar `main` (antes del workshop)

```bash
git checkout main

# DEBE tener:
ls notebooks/           # ✅ 6 notebooks
ls src/                 # ✅ Módulos básicos
ls data/                # ✅ Datos de ejemplo
ls scripts/             # ✅ verify_setup.py
ls .devcontainer/       # ✅ Configuración Codespaces
cat .env.example        # ✅ Solo placeholders
cat README.md           # ✅ Documentación

# NO DEBE tener:
ls solutions/           # ❌ No existe o está vacío
cat INSTRUCTOR_CHECKLIST.md  # ❌ No existe
cat .env                # ❌ No existe (está en .gitignore)
```

### Para Verificar `solutions` (tu referencia)

```bash
git checkout solutions

# DEBE tener TODO de main MÁS:
ls solutions/nivel_2_workshop/  # ✅ 7 soluciones + README
ls solutions/guias_instructor/  # ✅ 3 guías
cat INSTRUCTOR_CHECKLIST.md     # ✅ Existe
cat README_GITHUB_CODESPACES.md # ✅ Existe
cat BRANCH_STRUCTURE.md         # ✅ Este archivo
```

---

## 🚨 Errores Comunes a Evitar

### ❌ Error 1: Push de soluciones a `main`

```bash
# Verificar ANTES de push a main:
git checkout main
ls solutions/

# Si existe → PROBLEMA
# Solución:
git rm -r solutions/
git commit -m "Remove solutions from main"
git push origin main
```

### ❌ Error 2: API Key real en repo

```bash
# Verificar:
cat .env           # No debe existir en repo
cat .env.example   # Solo debe tener placeholders

# Si .env está en repo:
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "Remove .env from tracking"
git push
```

### ❌ Error 3: Archivos de instructor en `main`

```bash
# Estos NO deben estar en main:
ls INSTRUCTOR_CHECKLIST.md         # ❌
ls README_GITHUB_CODESPACES.md    # ❌
ls BRANCH_STRUCTURE.md            # ❌

# Si están:
git checkout main
git rm INSTRUCTOR_CHECKLIST.md README_GITHUB_CODESPACES.md BRANCH_STRUCTURE.md
git commit -m "Remove instructor-only files from main"
git push origin main
```

---

## 🎯 Antes del Workshop

### Checklist Final

**En `main` (participantes verán esto)**:
- [ ] Solo archivos necesarios para el workshop
- [ ] Carpeta `solutions/` NO existe
- [ ] `.env.example` solo con placeholders
- [ ] Documentación clara para empezar
- [ ] README.md actualizado con badge de Codespaces
- [ ] Push completo a GitHub

**En `solutions` (solo tú verás esto)**:
- [ ] Todos los archivos de `main`
- [ ] TODAS las soluciones completas
- [ ] Guías de instructor
- [ ] Documentación técnica adicional
- [ ] Push completo a GitHub

**GitHub Settings**:
- [ ] Rama `main` es la default
- [ ] Rama `solutions` existe pero no es default
- [ ] Configurar protección de rama `solutions` (opcional):
  - Settings → Branches → Add rule
  - Branch name pattern: `solutions`
  - Require pull request reviews (para que no borres accidentalmente)

---

## 📧 Para Compartir con Participantes

**Email**: "Accede al workshop en: https://github.com/[TU-USUARIO]/rag-workshop-2025"

**Ellos verán**:
- Rama `main` por defecto
- Notebooks para trabajar
- Ninguna solución
- Documentación clara de inicio

**NO verán**:
- Rama `solutions` (a menos que busquen específicamente)
- Archivos de instructor
- Soluciones completas

---

## 🛡️ Protección Adicional (Opcional)

### Hacer `solutions` privada con Git Submodule

Si quieres MÁS seguridad:

```bash
# 1. Crear repo separado solo para soluciones
# 2. En main repo, añadir como submodule:
git submodule add https://github.com/[TU-USUARIO]/rag-workshop-solutions.git solutions

# Ventaja: Repo de soluciones puede ser privado
# Desventaja: Más complejo de mantener
```

---

## 📚 Resumen Visual

```
┌─────────────────────────────────────────┐
│  RAMA: main (PÚBLICA)                   │
│  Para: PARTICIPANTES                    │
├─────────────────────────────────────────┤
│  ✅ Notebooks (con TODOs)               │
│  ✅ Código base                          │
│  ✅ Datos de ejemplo                     │
│  ✅ Scripts de verificación              │
│  ✅ Documentación de inicio              │
│  ❌ Sin soluciones                       │
│  ❌ Sin guías de instructor              │
└─────────────────────────────────────────┘
                    │
                    │ Sincronización selectiva
                    ↓
┌─────────────────────────────────────────┐
│  RAMA: solutions (PRIVADA)              │
│  Para: INSTRUCTORES                     │
├─────────────────────────────────────────┤
│  ✅ Todo lo de main                     │
│  ✅ + Soluciones completas (7 archivos) │
│  ✅ + Guías de instructor (3 archivos)  │
│  ✅ + Documentación técnica              │
│  ✅ + Checklists                         │
└─────────────────────────────────────────┘
```

---

**Última actualización**: 2025-10-01
**Autor**: Antonio Romero (aromero@secture.com)
