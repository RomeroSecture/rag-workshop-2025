# EJERCICIO 1: Optimizar chunk size - NIVEL 1 BÁSICO
# Solución mínima funcional

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from module_2_optimized import Module2_OptimizedRAG
import time

print("💪 EJERCICIO 1: Encuentra el chunk_size óptimo")
print("=" * 50)

chunk_sizes = [300, 500, 800, 1000, 1500]
results = []

for size in chunk_sizes:
    # Crear instancia con chunk size específico
    rag = Module2_OptimizedRAG()
    rag.chunk_size = size

    # Cargar y procesar documento
    doc = rag.load_document()
    chunks = rag.create_chunks(doc)
    rag.index_chunks(chunks[:20])

    # Medir tiempo de query
    start = time.time()
    response = rag.query("¿Cuál es la política de vacaciones?")
    elapsed = (time.time() - start) * 1000

    # Guardar resultado
    results.append({
        'size': size,
        'time': elapsed,
        'chunks': len(chunks)
    })

    print(f"Size {size}: {elapsed:.0f}ms, {len(chunks)} chunks")

# Encontrar el mejor
best = min(results, key=lambda x: x['time'])
print(f"\n✅ Mejor tamaño: {best['size']} ({best['time']:.0f}ms)")
