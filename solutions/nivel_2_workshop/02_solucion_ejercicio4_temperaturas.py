# EJERCICIO 4: Experimentar con temperaturas del LLM - NIVEL 2 WORKSHOP
# Celda 8 del notebook - Encontrar la temperatura óptima

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from module_2_optimized import Module2_OptimizedRAG
import time
import pandas as pd

print("💪 EJERCICIO 4: Experimentar con temperaturas del LLM")
print("=" * 60)

# Crear instancia RAG
rag = Module2_OptimizedRAG()

# Cargar y procesar documento
doc = rag.load_document()
chunks = rag.create_chunks(doc)
rag.index_chunks(chunks[:20])

# Queries de prueba (diferentes tipos)
test_queries = [
    "¿Cuáles son los beneficios de la empresa?",  # Factual
    "¿Qué opinas sobre el trabajo remoto?",       # Opinión (debería evitar)
    "Resume la política de vacaciones"            # Resumen
]

temperatures = [0.0, 0.3, 0.5, 0.7, 1.0]
results = []

print("\n🧪 Probando diferentes temperaturas...\n")

for temp in temperatures:
    print(f"\n{'='*60}")
    print(f"🌡️ TEMPERATURA: {temp}")
    print("="*60)

    # Configurar temperatura
    rag.temperature = temp

    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")

        # Ejecutar query
        start = time.time()
        response = rag.query(query)
        latency = (time.time() - start) * 1000

        answer = response.get('response', '')

        # Métricas
        print(f"   Respuesta ({len(answer)} chars): {answer[:120]}...")
        print(f"   Latencia: {latency:.0f}ms")

        # Analizar variabilidad (ejecutar 2 veces más para ver consistencia)
        if temp in [0.0, 0.7, 1.0]:  # Solo para algunos temps
            print(f"   Probando consistencia...")
            response2 = rag.query(query)
            answer2 = response2.get('response', '')

            # Calcular diferencia (simple: longitud y primeras palabras)
            len_diff = abs(len(answer) - len(answer2))
            words1 = set(answer[:100].split())
            words2 = set(answer2[:100].split())
            word_overlap = len(words1.intersection(words2)) / max(len(words1), len(words2))

            print(f"   Variabilidad: Δ{len_diff} chars, {word_overlap*100:.0f}% palabra overlap")

        results.append({
            'temperature': temp,
            'query_type': ['factual', 'opinion', 'summary'][i-1],
            'answer_length': len(answer),
            'latency_ms': round(latency, 0),
            'preview': answer[:60] + '...'
        })

        time.sleep(0.3)

# Análisis de resultados
print("\n\n📊 ANÁLISIS DE RESULTADOS")
print("=" * 60)

df = pd.DataFrame(results)

# Agrupar por temperatura
print("\n1️⃣ Longitud promedio de respuestas por temperatura:")
avg_by_temp = df.groupby('temperature')['answer_length'].mean()
print(avg_by_temp.to_string())

print("\n2️⃣ Latencia promedio por temperatura:")
latency_by_temp = df.groupby('temperature')['latency_ms'].mean()
print(latency_by_temp.to_string())

print("\n3️⃣ Comparación por tipo de query:")
for query_type in ['factual', 'opinion', 'summary']:
    print(f"\n   {query_type.upper()}:")
    subset = df[df['query_type'] == query_type]
    for _, row in subset.iterrows():
        print(f"   T={row['temperature']}: {row['preview']}")

# Recomendaciones
print("\n\n💡 RECOMENDACIONES:")
print("=" * 60)
print("""
🌡️ TEMPERATURA 0.0 (Determinista)
   ✅ Uso: Queries factuales, información precisa
   ✅ Ventajas: Consistencia 100%, reproducible
   ⚠️  Desventajas: Puede ser repetitivo

🌡️ TEMPERATURA 0.3 (Recomendado para RAG)
   ✅ Uso: Casos generales, balance ideal
   ✅ Ventajas: Consistente pero natural
   ✅ Perfecto para: Customer support, FAQs

🌡️ TEMPERATURA 0.7 (Creativo)
   ✅ Uso: Resúmenes, parafraseo
   ⚠️  Desventajas: Menos consistente
   ⚠️  Cuidado: Puede "adornar" facts

🌡️ TEMPERATURA 1.0 (Muy creativo)
   ❌ Evitar para RAG
   ❌ Riesgo: Alucinaciones frecuentes
   ✅ Solo si: Quieres diversidad en respuestas
""")

# Guardar configuración óptima
rag.temperature = 0.3
print(f"\n✅ Temperatura restaurada a 0.3 (óptimo para RAG)")

print("\n📋 CONCLUSIÓN:")
print("   Para sistemas RAG en producción: temperatura = 0.3")
print("   Es el mejor balance entre naturalidad y precisión factual")
