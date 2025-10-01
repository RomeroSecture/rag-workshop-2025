# 🔒 Seguridad de API Keys - Workshop RAG 2025

## ⚠️ IMPORTANTE: NO Compartir API Keys en Código

**Las API keys NUNCA deben estar en:**
- ❌ Código fuente (archivos .py, .ipynb)
- ❌ Commits de Git
- ❌ READMEs o documentación
- ❌ Capturas de pantalla compartidas
- ❌ Repos públicos de GitHub

---

## 🎓 Para Instructores: Manejo de API Keys en el Workshop

### OPCIÓN 1: Cada Participante Usa su Propia Key (RECOMENDADO)

**Ventajas**:
- ✅ Más seguro
- ✅ Sin límites de rate
- ✅ Aprenden mejores prácticas
- ✅ Pueden seguir practicando después

**Instrucciones para participantes**:
```
1. Crear cuenta en OpenAI: https://platform.openai.com/signup
2. Añadir $5 USD de créditos (Settings → Billing)
3. Crear API key: https://platform.openai.com/api-keys
4. Configurar en .env (ver abajo)
```

### OPCIÓN 2: API Key Compartida del Instructor

**Solo si algunos participantes no pueden obtener su propia key.**

**Pasos seguros**:

1. **Antes del workshop**:
   - Crear una API key NUEVA específica para el workshop
   - Configurar límites: Settings → Usage limits → Set max $20/month

2. **Durante el workshop**:
   - Compartir verbalmente o por chat privado (NO en pantalla proyectada)
   - Los participantes la configuran en su archivo `.env` local

3. **Después del workshop** (CRÍTICO):
   - **REVOCAR inmediatamente** la API key compartida
   - Go to: https://platform.openai.com/api-keys → Delete

**⚠️ NUNCA**:
- Compartir en Slack público / chat grupal que quede grabado
- Mostrar en pantalla durante presentaciones
- Incluir en código que se commitea a Git

---

## 👥 Para Participantes: Cómo Configurar tu API Key

### 1. Crear tu API Key de OpenAI

```
1. Ve a: https://platform.openai.com/signup
2. Crea cuenta (gratis)
3. Settings → Billing → Add payment method
4. Añade $5 USD (el workshop gasta ~$2-3)
5. API Keys → Create new secret key
6. COPIA la key (empieza con "sk-proj-" o "sk-")
   ⚠️ Solo la verás una vez!
7. Guárdala en un lugar seguro (password manager)
```

### 2. Configurar en tu Ambiente

**En GitHub Codespaces o Local**:

```bash
# 1. Copiar template
cp .env.example .env

# 2. Editar el archivo
nano .env  # o abrir con editor VSCode

# 3. Pegar tu API key
OPENAI_API_KEY=sk-proj-TU-API-KEY-COMPLETA-AQUI

# 4. Guardar y cerrar
```

**IMPORTANTE**:
- El archivo `.env` está en `.gitignore`
- NO se subirá a GitHub
- Es seguro poner tu key ahí

### 3. Verificar que Funciona

```bash
python scripts/verify_setup.py
```

Debes ver:
```
5️⃣ OpenAI API Key
✅ Configurada: sk-proj-...

6️⃣ Conexión con OpenAI
✅ Conexión exitosa (latencia: 234ms)
```

---

## 🚨 ¿Qué Hacer si tu API Key se Expone?

**Si accidentalmente subes tu API key a GitHub:**

### 1. Revócala INMEDIATAMENTE

```
1. Ve a: https://platform.openai.com/api-keys
2. Encuentra tu key expuesta
3. Click en "..." → Delete
4. Crea una nueva
```

### 2. Limpia el Historial de Git (si es necesario)

```bash
# Si está en el historial de commits:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Después, force push (¡cuidado!)
git push origin --force --all
```

### 3. Verifica en OpenAI Usage

```
Settings → Usage → Ver si hay actividad sospechosa
```

---

## 📊 Monitoreo de Uso Durante el Workshop

### Para Instructors (si usas key compartida)

```
1. Abre en otra pestaña:
   https://platform.openai.com/account/usage

2. Monitorea en tiempo real durante el workshop

3. Si ves uso anormal:
   - Revoca la key
   - Comparte una nueva
```

### Costos Esperados

**Por participante (8 horas de workshop)**:
- Módulo 1-2: ~$0.50 USD
- Módulo 3-4: ~$0.80 USD
- Módulo 5: ~$0.30 USD
- **Total**: ~$1.60 USD por persona

**Para 20 participantes**:
- Total: ~$32 USD
- Configurar límite: $50 USD (con margen)

---

## ✅ Checklist de Seguridad

**Antes del workshop**:
- [ ] Todos los archivos `.env` están en `.gitignore`
- [ ] No hay API keys hardcodeadas en código
- [ ] Template `.env.example` solo tiene placeholders
- [ ] Documentación NO incluye keys reales

**Durante el workshop**:
- [ ] Verificar que pantalla NO muestra archivo `.env`
- [ ] Compartir API key solo si es necesario (verbalmente)
- [ ] Recordar a participantes NO hacer screenshot de `.env`

**Después del workshop**:
- [ ] Revocar API key compartida (si se usó)
- [ ] Verificar que no se commiteó ningún `.env`
- [ ] Check usage en OpenAI

---

## 🎓 Educar a los Participantes

### Mensaje al Inicio del Workshop

```
"📢 IMPORTANTE SOBRE API KEYS:

Las API keys son como contraseñas:
- NUNCA las compartan en código
- NUNCA las suban a GitHub
- Úsenlas solo en archivos .env locales

El archivo .env está en .gitignore, así que es seguro
poner su API key ahí. Pero NUNCA la pongan en
notebooks (.ipynb) o scripts (.py).

Si accidentalmente exponen su key:
1. Revóquenla inmediatamente
2. Creen una nueva
3. Avísenme si necesitan ayuda

¿Preguntas sobre seguridad?"
```

---

## 📚 Recursos Adicionales

- [OpenAI Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Protecting API Keys](https://cloud.google.com/docs/authentication/api-keys)

---

## 🆘 Soporte

**Si tienes dudas sobre seguridad de API keys**:
- Email: aromero@secture.com
- Durante workshop: Pregunta al instructor

---

**Última actualización**: 2025-10-01
**Recuerda**: La seguridad de las API keys es responsabilidad de todos 🔒
