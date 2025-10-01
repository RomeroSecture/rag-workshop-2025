# EJERCICIO 2: Implementar filtrado por metadatos - NIVEL 2 WORKSHOP

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from module_2_optimized import Module2_OptimizedRAG
from typing import Dict, List, Any

print("💪 EJERCICIO 2: Filtrar resultados por metadatos")
print("=" * 50)

def filter_by_metadata(results: Dict, filter_criteria: Dict[str, Any]) -> Dict:
    """
    Filtra resultados basado en metadatos

    Args:
        results: Diccionario con 'documents' y 'metadatas'
        filter_criteria: Dict con criterios de filtrado (ej: {"section": "benefits"})

    Returns:
        Results filtrados con misma estructura
    """
    if not results or not results.get('documents'):
        return results

    filtered_docs = []
    filtered_metadata = []
    filtered_scores = []

    # Iterar sobre resultados
    for i, metadata in enumerate(results.get('metadatas', [])):
        # Verificar si cumple todos los criterios
        match = True
        for key, value in filter_criteria.items():
            if metadata.get(key) != value:
                match = False
                break

        if match:
            filtered_docs.append(results['documents'][i])
            filtered_metadata.append(metadata)
            if 'scores' in results and i < len(results['scores']):
                filtered_scores.append(results['scores'][i])

    return {
        'documents': filtered_docs,
        'metadatas': filtered_metadata,
        'scores': filtered_scores if filtered_scores else None
    }


# ===== TEST =====

# Crear instancia RAG
rag = Module2_OptimizedRAG()
doc = rag.load_document()
chunks = rag.create_chunks(doc)

# Indexar con metadatos enriquecidos
rag.index_chunks(chunks[:20])

# Búsqueda normal
query = "beneficios para empleados"
print(f"\n🔍 Query: {query}")

results = rag.search_with_rerank(query, k=10)
print(f"\n📊 Resultados sin filtro: {len(results['documents'])} documentos")

# Aplicar filtros
filter_criteria = {"section": "benefits"}
print(f"\n🔧 Aplicando filtro: {filter_criteria}")

filtered_results = filter_by_metadata(results, filter_criteria)
print(f"📊 Resultados filtrados: {len(filtered_results['documents'])} documentos")

# Mostrar resultados
print("\n✅ Top 3 resultados filtrados:")
for i, doc in enumerate(filtered_results['documents'][:3]):
    print(f"\n{i+1}. {doc[:100]}...")
    if filtered_results['metadatas']:
        print(f"   Metadata: {filtered_results['metadatas'][i]}")
