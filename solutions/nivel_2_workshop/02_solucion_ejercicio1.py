# EJERCICIO 1: Optimizar chunk size - NIVEL 2 WORKSHOP
# Solución esperada en el workshop con métricas de calidad

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from module_2_optimized import Module2_OptimizedRAG
from shared_config import TestSuite, Module
import time
import pandas as pd

print("💪 EJERCICIO 1: Encuentra el chunk_size óptimo")
print("=" * 50)

chunk_sizes = [300, 500, 800, 1000, 1500]
test_queries = [
    "¿Cuál es la política de vacaciones?",
    "¿Qué beneficios tienen los empleados senior?",
    "¿Cómo funciona el trabajo remoto?"
]

results = []

for size in chunk_sizes:
    print(f"\n🔧 Probando chunk_size={size}")

    # Crear instancia con chunk size específico
    rag = Module2_OptimizedRAG()
    rag.chunk_size = size

    # Cargar y procesar documento
    doc = rag.load_document()
    chunks = rag.create_chunks(doc)
    rag.index_chunks(chunks[:20])

    # Medir tiempo y calidad en múltiples queries
    times = []
    scores = []

    for query in test_queries:
        start = time.time()
        response = rag.query(query)
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)

        # Evaluar calidad
        eval_result = TestSuite.evaluate_response(response['response'], Module.OPTIMIZED)
        scores.append(eval_result['score'])

        time.sleep(0.5)

    # Promediar resultados
    avg_time = sum(times) / len(times)
    avg_score = sum(scores) / len(scores)

    results.append({
        'chunk_size': size,
        'num_chunks': len(chunks),
        'avg_latency_ms': round(avg_time, 0),
        'avg_quality': round(avg_score, 3),
        'combined_score': round(avg_score / (avg_time / 1000), 3)  # Calidad/segundo
    })

    print(f"  ⏱️ Latencia: {avg_time:.0f}ms")
    print(f"  🎯 Calidad: {avg_score:.3f}")
    print(f"  📦 Chunks: {len(chunks)}")

# Mostrar tabla de resultados
print("\n📊 RESULTADOS COMPARATIVOS:")
print("=" * 70)
df = pd.DataFrame(results)
print(df.to_string(index=False))

# Análisis y recomendación
best_balanced = max(results, key=lambda x: x['combined_score'])
best_latency = min(results, key=lambda x: x['avg_latency_ms'])
best_quality = max(results, key=lambda x: x['avg_quality'])

print("\n🎯 ANÁLISIS:")
print(f"✅ Mejor balance calidad/latencia: {best_balanced['chunk_size']}")
print(f"⚡ Más rápido: {best_latency['chunk_size']} ({best_latency['avg_latency_ms']:.0f}ms)")
print(f"🏆 Mejor calidad: {best_quality['chunk_size']} (score: {best_quality['avg_quality']:.3f})")

print("\n💡 RECOMENDACIÓN:")
print(f"   Para casos de uso general: chunk_size={best_balanced['chunk_size']}")
print(f"   Para respuestas rápidas: chunk_size={best_latency['chunk_size']}")
print(f"   Para máxima precisión: chunk_size={best_quality['chunk_size']}")
