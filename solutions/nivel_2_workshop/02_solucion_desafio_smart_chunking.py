# DESAFÍO ADICIONAL: Smart Chunking - NIVEL 2 WORKSHOP
# Celda 18 del notebook - Chunking inteligente que respeta límites de frases

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from typing import List
import re

print("💪 DESAFÍO: Smart Chunking con límites de frases")
print("=" * 60)


def smart_chunking(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Chunking inteligente que:
    - No corta frases a la mitad
    - Respeta párrafos cuando sea posible
    - Mantiene contexto entre chunks con overlap

    Args:
        text: Texto a dividir
        chunk_size: Tamaño objetivo del chunk
        overlap: Caracteres de overlap entre chunks

    Returns:
        Lista de chunks
    """
    # Limpiar texto
    text = text.strip()

    # Detectar límites de frases (., !, ?, \n\n)
    sentence_endings = r'[.!?]\s+|\n\n'

    # Dividir en frases
    sentences = re.split(sentence_endings, text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    current_chunk = ""
    previous_chunk_end = ""

    for sentence in sentences:
        # Si añadir esta frase excede el tamaño
        if len(current_chunk) + len(sentence) > chunk_size:
            # Si el chunk actual tiene contenido, guardarlo
            if current_chunk:
                # Añadir overlap del chunk anterior
                if previous_chunk_end:
                    full_chunk = previous_chunk_end + " " + current_chunk
                else:
                    full_chunk = current_chunk

                chunks.append(full_chunk.strip())

                # Guardar overlap para el siguiente chunk
                words = current_chunk.split()
                overlap_words = []
                overlap_chars = 0

                # Tomar últimas palabras hasta completar overlap
                for word in reversed(words):
                    if overlap_chars + len(word) < overlap:
                        overlap_words.insert(0, word)
                        overlap_chars += len(word) + 1
                    else:
                        break

                previous_chunk_end = " ".join(overlap_words)

                # Empezar nuevo chunk con la frase actual
                current_chunk = sentence
            else:
                # Si una sola frase es muy larga, dividirla por palabras
                if len(sentence) > chunk_size * 1.5:
                    words = sentence.split()
                    temp_chunk = ""

                    for word in words:
                        if len(temp_chunk) + len(word) > chunk_size:
                            if temp_chunk:
                                chunks.append(temp_chunk.strip())
                                temp_chunk = word
                        else:
                            temp_chunk += " " + word if temp_chunk else word

                    current_chunk = temp_chunk
                else:
                    current_chunk = sentence
        else:
            # Añadir frase al chunk actual
            current_chunk += " " + sentence if current_chunk else sentence

    # Añadir último chunk
    if current_chunk:
        if previous_chunk_end:
            full_chunk = previous_chunk_end + " " + current_chunk
        else:
            full_chunk = current_chunk
        chunks.append(full_chunk.strip())

    return chunks


# ===== TEST Y COMPARACIÓN =====

# Texto de ejemplo con frases cortadas
test_text = """
La política de vacaciones de la empresa es clara. Todos los empleados tienen derecho a vacaciones pagadas.

Los empleados nuevos (0-5 años) reciben 22 días hábiles al año. Los empleados senior (5-10 años) reciben 25 días hábiles. Los empleados veteranos (más de 10 años) reciben 30 días hábiles.

Además, hay días adicionales por antigüedad. Por cada 5 años adicionales, se otorgan 2 días extra. Los empleados pueden comprar hasta 5 días adicionales de vacaciones por año.

Las vacaciones deben solicitarse con al menos 2 semanas de anticipación. La aprobación está sujeta a las necesidades del equipo y la disponibilidad de personal.
"""

print("\n1️⃣ CHUNKING BÁSICO (sin smart chunking):")
print("="*60)

# Chunking básico (corta en cualquier posición)
basic_chunks = []
chunk_size = 150
for i in range(0, len(test_text), chunk_size):
    basic_chunks.append(test_text[i:i+chunk_size])

for i, chunk in enumerate(basic_chunks, 1):
    print(f"\nChunk {i} ({len(chunk)} chars):")
    print(f"'{chunk}'")
    # Detectar si corta a mitad de frase
    if not chunk.rstrip().endswith(('.', '!', '?', '\n')):
        print("   ⚠️  CORTADO A MITAD DE FRASE")

print("\n\n2️⃣ SMART CHUNKING (respeta límites):")
print("="*60)

smart_chunks = smart_chunking(test_text, chunk_size=150, overlap=30)

for i, chunk in enumerate(smart_chunks, 1):
    print(f"\nChunk {i} ({len(chunk)} chars):")
    print(f"'{chunk}'")

    # Verificar que termina en límite de frase
    ends_properly = chunk.rstrip().endswith(('.', '!', '?')) or '\n\n' in chunk
    if ends_properly:
        print("   ✅ Termina correctamente")
    else:
        print("   ⚠️  No termina en límite de frase")

# Comparación de métricas
print("\n\n📊 COMPARACIÓN:")
print("="*60)
print(f"Chunking Básico:")
print(f"   - Total chunks: {len(basic_chunks)}")
print(f"   - Tamaño promedio: {sum(len(c) for c in basic_chunks) / len(basic_chunks):.0f} chars")
print(f"   - Chunks cortados: {sum(1 for c in basic_chunks if not c.rstrip().endswith(('.', '!', '?', '\n')))}")

print(f"\nSmart Chunking:")
print(f"   - Total chunks: {len(smart_chunks)}")
print(f"   - Tamaño promedio: {sum(len(c) for c in smart_chunks) / len(smart_chunks):.0f} chars")
print(f"   - Chunks cortados: {sum(1 for c in smart_chunks if not c.rstrip().endswith(('.', '!', '?')))}")

# Verificar overlap
print(f"\n🔗 Verificación de overlap:")
for i in range(len(smart_chunks) - 1):
    # Encontrar overlap entre chunks consecutivos
    chunk1_end = smart_chunks[i][-50:]  # Últimos 50 chars
    chunk2_start = smart_chunks[i+1][:50]  # Primeros 50 chars

    # Buscar palabras comunes
    words1 = set(chunk1_end.split())
    words2 = set(chunk2_start.split())
    overlap_words = words1.intersection(words2)

    if overlap_words:
        print(f"   Chunks {i+1}-{i+2}: {len(overlap_words)} palabras compartidas")
    else:
        print(f"   Chunks {i+1}-{i+2}: Sin overlap detectado")

print("\n\n💡 BENEFICIOS DEL SMART CHUNKING:")
print("="*60)
print("""
✅ Preserva el significado completo de las frases
✅ Mejora la comprensión del contexto
✅ Reduce fragmentación de información
✅ Mantiene coherencia temática
✅ Facilita el retrieval semántico más preciso

🎯 Ideal para:
   - Documentos técnicos con procedimientos paso a paso
   - Manuales con instrucciones específicas
   - Documentos legales donde cada frase es importante
   - FAQs donde cada pregunta/respuesta es una unidad completa
""")

# Integración con RAG
print("\n🔧 INTEGRACIÓN CON RAG:")
print("="*60)
print("""
Para usar smart_chunking en tu RAG:

1. Reemplaza el método create_chunks() en tu clase RAG:

   class MyRAG(Module2_OptimizedRAG):
       def create_chunks(self, text: str) -> List[str]:
           return smart_chunking(
               text,
               chunk_size=self.chunk_size,
               overlap=self.chunk_overlap
           )

2. Prueba con tus documentos reales

3. Compara métricas de calidad vs chunking básico
""")
