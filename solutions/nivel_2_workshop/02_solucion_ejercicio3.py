# EJERCICIO 3: Crear un prompt especializado - NIVEL 2 WORKSHOP

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from module_2_optimized import Module2_OptimizedRAG

print("💪 EJERCICIO 3: Diseña un prompt para queries técnicas")
print("=" * 50)

# Prompt optimizado para queries técnicas
technical_prompt = """
Eres un especialista en soporte técnico IT analizando documentación técnica corporativa.

DOCUMENTACIÓN RELEVANTE:
{context}

CONSULTA TÉCNICA:
{question}

INSTRUCCIONES:
1. Proporciona SOLO información basada en la documentación
2. Si requiere configuración, usa formato de código:
   ```
   parámetro: valor
   ```
3. Incluye advertencias de seguridad si aplica
4. Si la info está incompleta, indica claramente qué falta
5. Estructura la respuesta así:
   - Respuesta directa (1-2 líneas)
   - Pasos de configuración (si aplica)
   - Notas adicionales

RESPUESTA TÉCNICA:
"""

# Test del prompt
rag = Module2_OptimizedRAG()
doc = rag.load_document()
chunks = rag.create_chunks(doc)
rag.index_chunks(chunks[:20])

# Sobrescribir el prompt
rag.prompt_template = technical_prompt

# Query técnica
query = "¿Cómo configuro el VPN de la empresa?"

print(f"\n🔍 Query técnica: {query}")
print("\n⏳ Generando respuesta con prompt técnico...")

result = rag.query(query)

print("\n✅ RESPUESTA:")
print("=" * 60)
print(result['response'])
print("=" * 60)

print(f"\n📊 Métricas:")
print(f"   Tiempo: {result['metrics']['total_time_ms']:.0f}ms")
print(f"   Sources: {result['metrics']['num_sources']}")

# Comparar con prompt genérico
print("\n🔄 Comparando con prompt genérico...")
rag.prompt_template = """
Contexto: {context}
Pregunta: {question}
Responde basándote en el contexto.
"""

result_generic = rag.query(query)

print("\n📝 RESPUESTA CON PROMPT GENÉRICO:")
print("=" * 60)
print(result_generic['response'])
print("=" * 60)

print("\n💡 DIFERENCIAS:")
print("✅ Prompt técnico: Formato estructurado, código resaltado, advertencias")
print("❌ Prompt genérico: Respuesta sin estructura específica")
