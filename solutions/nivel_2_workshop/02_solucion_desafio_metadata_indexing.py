# DESAFÍO ADICIONAL: Indexación con Metadata - NIVEL 2 WORKSHOP
# Celda 18 del notebook - Añadir metadatos enriquecidos para mejor trazabilidad

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from typing import List, Dict, Any
from datetime import datetime
import hashlib

print("💪 DESAFÍO: Indexación con Metadata Enriquecidos")
print("=" * 60)


def extract_metadata_from_chunk(
    chunk: str,
    chunk_id: int,
    source_doc: str,
    total_chunks: int
) -> Dict[str, Any]:
    """
    Extrae y construye metadata enriquecidos para un chunk

    Args:
        chunk: Texto del chunk
        chunk_id: ID numérico del chunk
        source_doc: Documento fuente
        total_chunks: Total de chunks del documento

    Returns:
        Dict con metadata enriquecidos
    """
    metadata = {}

    # === METADATA BÁSICOS ===
    metadata['chunk_id'] = chunk_id
    metadata['source_document'] = Path(source_doc).name
    metadata['chunk_position'] = f"{chunk_id + 1}/{total_chunks}"

    # === METADATA DE CONTENIDO ===
    metadata['length_chars'] = len(chunk)
    metadata['length_words'] = len(chunk.split())

    # Detectar sección del documento (basado en keywords)
    section = detect_section(chunk)
    metadata['section'] = section

    # Detectar tipo de contenido
    content_type = detect_content_type(chunk)
    metadata['content_type'] = content_type

    # === METADATA TÉCNICOS ===
    # Hash único del chunk para deduplicación
    metadata['content_hash'] = hashlib.md5(chunk.encode()).hexdigest()

    # Timestamp de indexación
    metadata['indexed_at'] = datetime.now().isoformat()

    # Versión del documento (útil para updates)
    metadata['doc_version'] = "1.0"

    # === METADATA DE CALIDAD ===
    # Score de completitud (tiene frases completas?)
    metadata['completeness_score'] = calculate_completeness(chunk)

    # Densidad de información (ratio keywords/total words)
    metadata['info_density'] = calculate_info_density(chunk)

    return metadata


def detect_section(chunk: str) -> str:
    """
    Detecta la sección del documento basándose en keywords
    """
    chunk_lower = chunk.lower()

    section_keywords = {
        'benefits': ['beneficio', 'seguro', 'pensión', 'compensación'],
        'vacation': ['vacaciones', 'días libres', 'ausencia', 'permiso'],
        'remote_work': ['remoto', 'teletrabajo', 'home office', 'trabajo desde casa'],
        'onboarding': ['onboarding', 'inducción', 'nuevos empleados', 'bienvenida'],
        'policies': ['política', 'regla', 'norma', 'procedimiento'],
        'technical': ['configuración', 'vpn', 'sistema', 'software', 'hardware'],
    }

    for section, keywords in section_keywords.items():
        if any(keyword in chunk_lower for keyword in keywords):
            return section

    return 'general'


def detect_content_type(chunk: str) -> str:
    """
    Detecta el tipo de contenido del chunk
    """
    # Detectar listas
    if '•' in chunk or chunk.count('\n-') > 2 or chunk.count('\n*') > 2:
        return 'list'

    # Detectar tablas (múltiples | o tabs)
    if chunk.count('|') > 5 or chunk.count('\t') > 5:
        return 'table'

    # Detectar código o configuración
    if '```' in chunk or chunk.count('=') > 5:
        return 'code'

    # Detectar preguntas/respuestas
    if '?' in chunk and chunk.count('?') <= 3:
        return 'qa'

    # Detectar párrafos narrativos
    if chunk.count('.') > 3:
        return 'narrative'

    return 'mixed'


def calculate_completeness(chunk: str) -> float:
    """
    Calcula score de completitud (0-1)
    Chunks con frases completas tienen score más alto
    """
    # Contar frases completas
    complete_sentences = chunk.count('.') + chunk.count('!') + chunk.count('?')

    # Verificar si empieza con mayúscula
    starts_properly = chunk[0].isupper() if chunk else False

    # Verificar si termina con puntuación
    ends_properly = chunk.rstrip()[-1] in '.!?' if chunk else False

    # Score combinado
    score = 0.0
    if complete_sentences > 0:
        score += 0.5
    if starts_properly:
        score += 0.25
    if ends_properly:
        score += 0.25

    return round(score, 2)


def calculate_info_density(chunk: str) -> float:
    """
    Calcula densidad de información (0-1)
    Basado en ratio de palabras informativas vs total
    """
    # Palabras informativas (sustantivos, verbos importantes)
    informative_keywords = [
        'empleado', 'política', 'beneficio', 'vacaciones', 'día',
        'empresa', 'año', 'proceso', 'solicitud', 'remoto', 'trabajo'
    ]

    words = chunk.lower().split()
    if not words:
        return 0.0

    # Contar keywords informativos
    info_words = sum(1 for word in words if any(kw in word for kw in informative_keywords))

    # Ratio
    density = info_words / len(words)

    return round(min(density, 1.0), 2)


def index_chunks_with_metadata(
    chunks: List[str],
    source_doc: str = "document.pdf"
) -> List[Dict[str, Any]]:
    """
    Indexa chunks con metadata enriquecidos

    Returns:
        Lista de dicts con 'text' y 'metadata'
    """
    indexed_chunks = []

    for i, chunk in enumerate(chunks):
        metadata = extract_metadata_from_chunk(
            chunk=chunk,
            chunk_id=i,
            source_doc=source_doc,
            total_chunks=len(chunks)
        )

        indexed_chunks.append({
            'text': chunk,
            'metadata': metadata
        })

    return indexed_chunks


# ===== TEST Y DEMOSTRACIÓN =====

# Chunks de ejemplo
test_chunks = [
    """
La política de vacaciones de la empresa es clara y justa. Todos los empleados tienen derecho a vacaciones pagadas según su antigüedad.
    """,
    """
Beneficios incluidos:
• Seguro médico completo
• Seguro dental y visión
• Plan de pensiones con match del 5%
• Bonos anuales por desempeño
    """,
    """
Para configurar el VPN:
1. Descarga el cliente OpenVPN
2. Importa el archivo .ovpn
3. Ingresa tus credenciales corporativas
4. Conecta al servidor vpn.company.com
    """,
    """
¿Cómo solicito trabajo remoto? El proceso es simple: envía un email a tu manager con al menos 2 semanas de anticipación.
    """
]

print("\n🔍 PROCESANDO CHUNKS CON METADATA...")
print("=" * 60)

indexed_chunks = index_chunks_with_metadata(
    test_chunks,
    source_doc="company_handbook.pdf"
)

for i, item in enumerate(indexed_chunks, 1):
    print(f"\n{'='*60}")
    print(f"CHUNK {i}")
    print("="*60)

    print(f"\n📝 Texto ({len(item['text'])} chars):")
    print(item['text'][:150] + '...' if len(item['text']) > 150 else item['text'])

    print(f"\n📋 Metadata:")
    for key, value in item['metadata'].items():
        print(f"   {key:20s}: {value}")

# Análisis agregado
print("\n\n📊 ANÁLISIS AGREGADO DE METADATA:")
print("=" * 60)

# Agrupar por sección
sections = {}
for item in indexed_chunks:
    section = item['metadata']['section']
    sections[section] = sections.get(section, 0) + 1

print("\n1️⃣ Distribución por sección:")
for section, count in sections.items():
    print(f"   {section:15s}: {count} chunks")

# Agrupar por tipo de contenido
content_types = {}
for item in indexed_chunks:
    ctype = item['metadata']['content_type']
    content_types[ctype] = content_types.get(ctype, 0) + 1

print("\n2️⃣ Distribución por tipo de contenido:")
for ctype, count in content_types.items():
    print(f"   {ctype:15s}: {count} chunks")

# Métricas de calidad
avg_completeness = sum(item['metadata']['completeness_score'] for item in indexed_chunks) / len(indexed_chunks)
avg_density = sum(item['metadata']['info_density'] for item in indexed_chunks) / len(indexed_chunks)

print(f"\n3️⃣ Métricas de calidad promedio:")
print(f"   Completeness: {avg_completeness:.2f}/1.0")
print(f"   Info density: {avg_density:.2f}/1.0")

# Casos de uso de metadata
print("\n\n🎯 CASOS DE USO DE METADATA:")
print("=" * 60)

print("""
1️⃣ FILTRADO AVANZADO:
   - Buscar solo en sección 'benefits'
   - Excluir chunks con baja densidad de info
   - Filtrar por tipo de contenido (ej: solo listas)

2️⃣ RE-RANKING MEJORADO:
   - Priorizar chunks con alta completeness
   - Boost a secciones específicas según la query
   - Penalizar chunks muy cortos o incompletos

3️⃣ TRAZABILIDAD:
   - Saber exactamente de dónde viene cada respuesta
   - Tracking de versiones de documentos
   - Auditoría de qué información se está usando

4️⃣ MANTENIMIENTO:
   - Detectar chunks duplicados por hash
   - Identificar chunks que necesitan re-indexación
   - Monitorear calidad de la base de conocimiento

5️⃣ ANALYTICS:
   - Qué secciones se consultan más
   - Qué tipo de contenido es más útil
   - Gaps en la documentación
""")

# Ejemplo de query con filtros de metadata
print("\n🔧 EJEMPLO: Query con filtros de metadata")
print("=" * 60)

print("""
# Buscar solo en sección de beneficios con alta densidad

query = "¿Qué seguros ofrece la empresa?"

results = vectordb.search(
    query_embedding=embed(query),
    k=10,
    filter={
        "section": "benefits",
        "info_density": {"$gte": 0.3},
        "content_type": {"$in": ["list", "narrative"]}
    }
)

# Resultado: Solo chunks relevantes de beneficios,
# bien estructurados y con alta densidad de información
""")

print("\n💡 INTEGRACIÓN CON RAG:")
print("=" * 60)
print("""
Para integrar metadata enriquecidos en tu RAG:

1. Modifica el método index_chunks():

   def index_chunks(self, chunks: List[str]):
       indexed = index_chunks_with_metadata(chunks, self.doc_path)

       for item in indexed:
           self.vectordb.add(
               text=item['text'],
               metadata=item['metadata']
           )

2. Usa metadata en búsquedas:

   def search_with_filters(self, query: str, filters: dict):
       results = self.vectordb.search(
           query=query,
           k=5,
           filter=filters
       )
       return results

3. Enriquece respuestas con metadata:

   def query(self, question: str):
       results = self.search(question)

       # Añadir metadata a la respuesta
       response = self.llm.generate(question, results)
       response['sources'] = [
           {
               'text': r['text'][:100],
               'section': r['metadata']['section'],
               'source': r['metadata']['source_document']
           }
           for r in results
       ]

       return response
""")
