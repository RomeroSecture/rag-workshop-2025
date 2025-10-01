# DESAFÍO ADICIONAL: Re-ranking Avanzado - NIVEL 2 WORKSHOP
# Celda 18 del notebook - Implementar re-ranking para mejorar relevancia

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from typing import List, Dict, Any, Tuple
import numpy as np

print("💪 DESAFÍO: Re-ranking Avanzado de Resultados")
print("=" * 60)


def calculate_keyword_score(query: str, document: str) -> float:
    """
    Score basado en coincidencia de keywords (BM25 simplificado)

    Returns:
        Score entre 0 y 1
    """
    query_words = set(query.lower().split())
    doc_words = document.lower().split()
    doc_word_set = set(doc_words)

    # Exact match score
    matches = query_words.intersection(doc_word_set)
    if not query_words:
        return 0.0

    exact_match_score = len(matches) / len(query_words)

    # Frequency score (palabras importantes aparecen más)
    freq_score = 0.0
    for word in matches:
        freq = doc_words.count(word)
        # TF normalizado
        freq_score += min(freq / len(doc_words), 0.3)

    # Combinación
    combined_score = (exact_match_score * 0.6) + (freq_score * 0.4)

    return round(min(combined_score, 1.0), 3)


def calculate_position_score(chunk_position: int, total_chunks: int) -> float:
    """
    Score basado en posición del chunk
    Chunks al inicio del documento suelen ser más importantes (introducción)

    Returns:
        Score entre 0 y 1
    """
    # Decaimiento logarítmico
    position_ratio = chunk_position / max(total_chunks, 1)

    # Chunks iniciales tienen score más alto
    if position_ratio < 0.2:  # Primeros 20%
        return 1.0
    elif position_ratio < 0.5:  # Primeros 50%
        return 0.8
    else:
        return 0.6


def calculate_length_score(chunk_length: int, optimal_length: int = 500) -> float:
    """
    Score basado en longitud del chunk
    Chunks cercanos a la longitud óptima tienen mejor score

    Returns:
        Score entre 0 and 1
    """
    # Distribución gaussiana centrada en optimal_length
    diff = abs(chunk_length - optimal_length)
    sigma = optimal_length * 0.5  # Desviación estándar

    score = np.exp(-(diff ** 2) / (2 * sigma ** 2))

    # Penalizar chunks muy cortos (< 100 chars)
    if chunk_length < 100:
        score *= 0.5

    return round(score, 3)


def calculate_completeness_score(chunk: str) -> float:
    """
    Score basado en completitud del chunk
    Frases completas tienen mejor score

    Returns:
        Score entre 0 and 1
    """
    # Contar puntuación de fin de frase
    sentence_endings = chunk.count('.') + chunk.count('!') + chunk.count('?')

    # Verificar que empieza con mayúscula
    starts_with_capital = chunk[0].isupper() if chunk else False

    # Verificar que termina con puntuación
    ends_with_punctuation = chunk.rstrip()[-1] in '.!?\\n' if chunk else False

    # Score combinado
    score = 0.0

    if sentence_endings > 0:
        score += 0.4

    if sentence_endings >= 2:  # Múltiples frases completas
        score += 0.2

    if starts_with_capital:
        score += 0.2

    if ends_with_punctuation:
        score += 0.2

    return round(score, 3)


def rerank_results(
    query: str,
    results: List[Dict[str, Any]],
    weights: Dict[str, float] = None
) -> List[Dict[str, Any]]:
    """
    Re-rankea resultados usando múltiples señales

    Args:
        query: Query original del usuario
        results: Lista de resultados con 'text', 'score', 'metadata'
        weights: Pesos para cada componente del score

    Returns:
        Resultados re-rankeados con nuevo score
    """
    if weights is None:
        weights = {
            'semantic': 0.40,      # Score semántico original
            'keyword': 0.25,       # Coincidencia de keywords
            'position': 0.10,      # Posición en documento
            'length': 0.10,        # Longitud del chunk
            'completeness': 0.15   # Completitud del chunk
        }

    reranked_results = []

    for result in results:
        text = result.get('text', '')
        semantic_score = result.get('score', 0.0)
        metadata = result.get('metadata', {})

        # Calcular scores individuales
        keyword_score = calculate_keyword_score(query, text)

        position = metadata.get('chunk_id', 0)
        total_chunks = metadata.get('total_chunks', 1)
        position_score = calculate_position_score(position, total_chunks)

        length = len(text)
        length_score = calculate_length_score(length)

        completeness_score = calculate_completeness_score(text)

        # Score final ponderado
        final_score = (
            semantic_score * weights['semantic'] +
            keyword_score * weights['keyword'] +
            position_score * weights['position'] +
            length_score * weights['length'] +
            completeness_score * weights['completeness']
        )

        # Guardar resultado con scores desglosados
        reranked_result = result.copy()
        reranked_result['rerank_score'] = round(final_score, 4)
        reranked_result['score_breakdown'] = {
            'semantic': round(semantic_score, 3),
            'keyword': round(keyword_score, 3),
            'position': round(position_score, 3),
            'length': round(length_score, 3),
            'completeness': round(completeness_score, 3),
        }

        reranked_results.append(reranked_result)

    # Ordenar por score final
    reranked_results.sort(key=lambda x: x['rerank_score'], reverse=True)

    return reranked_results


# ===== TEST Y DEMOSTRACIÓN =====

# Resultados simulados de búsqueda vectorial
mock_results = [
    {
        'text': """La empresa ofrece múltiples beneficios. Seguro médico completo para empleados y familia. Plan dental y de visión incluido.""",
        'score': 0.85,
        'metadata': {'chunk_id': 5, 'total_chunks': 20, 'section': 'benefits'}
    },
    {
        'text': """Beneficios adicionales incluyen: seguro de vida, plan de pensiones con match del 5%, bonos anuales.""",
        'score': 0.82,
        'metadata': {'chunk_id': 6, 'total_chunks': 20, 'section': 'benefits'}
    },
    {
        'text': """Para empleados senior con más de 5 años, beneficios especiales: días extra de vacaciones, seguro premium.""",
        'score': 0.80,
        'metadata': {'chunk_id': 15, 'total_chunks': 20, 'section': 'benefits'}
    },
    {
        'text': """Los beneficios se activan después del período de prueba de 3 meses. Contacta a RH para más detalles""",
        'score': 0.75,
        'metadata': {'chunk_id': 7, 'total_chunks': 20, 'section': 'onboarding'}
    },
    {
        'text': """Seg""",  # Chunk incompleto
        'score': 0.78,
        'metadata': {'chunk_id': 8, 'total_chunks': 20, 'section': 'benefits'}
    },
]

query = "beneficios para empleados senior"

print("\n🔍 QUERY:", query)
print("=" * 60)

print("\n1️⃣ RESULTADOS ORIGINALES (solo score semántico):")
print("-" * 60)

for i, result in enumerate(mock_results, 1):
    print(f"\n#{i} - Score: {result['score']:.3f}")
    print(f"   Texto: {result['text'][:80]}...")
    print(f"   Metadata: {result['metadata']}")

# Aplicar re-ranking
print("\n\n2️⃣ RESULTADOS RE-RANKEADOS (multi-señal):")
print("-" * 60)

reranked = rerank_results(query, mock_results)

for i, result in enumerate(reranked, 1):
    print(f"\n#{i} - Rerank Score: {result['rerank_score']:.4f}")
    print(f"   Texto: {result['text'][:80]}...")

    print(f"   Score Breakdown:")
    for component, score in result['score_breakdown'].items():
        print(f"      {component:12s}: {score:.3f}")

    # Mostrar cambio de posición
    original_pos = mock_results.index(
        next(r for r in mock_results if r['text'] == result['text'])
    ) + 1
    if original_pos != i:
        direction = "↑" if original_pos > i else "↓"
        print(f"   Cambio: Posición {original_pos} → {i} {direction}")

# Análisis de mejoras
print("\n\n📊 ANÁLISIS DE RE-RANKING:")
print("=" * 60)

print("\n🎯 Mejoras observadas:")

# Chunk incompleto penalizado
incomplete_chunk = next(r for r in reranked if len(r['text']) < 50)
print(f"\n1. Chunk incompleto penalizado:")
print(f"   Original score: {next(r['score'] for r in mock_results if r['text'] == incomplete_chunk['text']):.3f}")
print(f"   Rerank score: {incomplete_chunk['rerank_score']:.4f}")
print(f"   Razón: Baja completeness ({incomplete_chunk['score_breakdown']['completeness']:.3f})")

# Keyword match mejorado
senior_chunk = next((r for r in reranked if 'senior' in r['text']), None)
if senior_chunk:
    print(f"\n2. Chunk con keyword 'senior' potenciado:")
    original_score = next(r['score'] for r in mock_results if r['text'] == senior_chunk['text'])
    print(f"   Original score: {original_score:.3f}")
    print(f"   Rerank score: {senior_chunk['rerank_score']:.4f}")
    print(f"   Keyword match: {senior_chunk['score_breakdown']['keyword']:.3f}")

print("\n\n💡 VENTAJAS DEL RE-RANKING:")
print("=" * 60)
print("""
✅ Combina múltiples señales de relevancia
✅ Penaliza chunks incompletos o mal formados
✅ Potencia matches exactos de keywords importantes
✅ Considera contexto del documento (posición)
✅ Mejora precision@k de los resultados

🎯 Casos de uso ideales:
   - Queries con keywords específicos importantes
   - Documentos largos donde la posición importa
   - Necesidad de alta precisión en top-3 resultados
   - Filtrado de chunks de baja calidad
""")

# Configuraciones personalizadas
print("\n🔧 CONFIGURACIONES PERSONALIZADAS:")
print("=" * 60)

configs = {
    'balanced': {
        'semantic': 0.40, 'keyword': 0.25, 'position': 0.10,
        'length': 0.10, 'completeness': 0.15
    },
    'keyword_focused': {
        'semantic': 0.30, 'keyword': 0.40, 'position': 0.05,
        'length': 0.10, 'completeness': 0.15
    },
    'quality_focused': {
        'semantic': 0.35, 'keyword': 0.20, 'position': 0.05,
        'length': 0.15, 'completeness': 0.25
    },
}

print("\nConfigs disponibles:")
for name, weights in configs.items():
    print(f"\n{name}:")
    for component, weight in weights.items():
        print(f"   {component:12s}: {weight:.2f}")

print("\n\n🔌 INTEGRACIÓN CON RAG:")
print("=" * 60)
print("""
def query_with_reranking(self, question: str, k: int = 5):
    # 1. Búsqueda vectorial (recuperar más resultados)
    initial_results = self.vectordb.search(question, k=k*2)

    # 2. Re-ranking
    reranked = rerank_results(
        query=question,
        results=initial_results,
        weights=self.rerank_weights  # Configuración personalizada
    )

    # 3. Tomar top-k re-rankeados
    top_results = reranked[:k]

    # 4. Generar respuesta con contexto mejorado
    context = "\\n\\n".join([r['text'] for r in top_results])
    answer = self.llm.generate(question, context)

    return {
        'answer': answer,
        'sources': top_results,
        'rerank_metrics': {
            'initial_results': len(initial_results),
            'top_score_improvement': (
                top_results[0]['rerank_score'] -
                top_results[0]['score']
            )
        }
    }
""")
