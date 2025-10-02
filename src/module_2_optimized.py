"""
Módulo 2: RAG Optimizado
Extiende el Módulo 1 con optimizaciones de rendimiento
"""

import os
import time
import hashlib
import json
from typing import List, Dict, Optional, Any, Tuple
from collections import OrderedDict
import numpy as np

# Deshabilitar telemetría de ChromaDB
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from module_1_basics import Module1_BasicRAG
from shared_config import RAGMasterConfig, Module, measure_performance


class LRUCache:
    """Cache LRU simple para queries"""

    def __init__(self, capacity: int = 100):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            # Mover al final (más reciente)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key: str, value: Any):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Eliminar el más antiguo
            self.cache.popitem(last=False)

    def clear(self):
        self.cache.clear()


class Module2_OptimizedRAG(Module1_BasicRAG):
    """
    Versión 2: RAG Optimizado con cache, overlap y re-ranking
    Extiende Module1 para mantener compatibilidad
    """

    def __init__(self):
        """Inicializar con optimizaciones adicionales"""
        # Heredar de Module1 pero skip la creación de colección
        super().__init__(skip_collection_setup=True)

        # Actualizar configuración para Módulo 2
        self.module = Module.OPTIMIZED
        self.chunk_size = self.config.chunking_params[self.module]["size"]
        self.chunk_overlap = self.config.chunking_params[self.module]["overlap"]

        # Cache para queries
        self.query_cache = LRUCache(capacity=50)
        self.embedding_cache = LRUCache(capacity=200)

        # Configuración adicional
        self.temperature = 0.3
        self.use_cache = True
        self.use_reranking = True

        # Crear colección para módulo 2
        collection_name = f"{self.config.COLLECTION_NAME}_module2"

        # Eliminar colección existente si existe
        try:
            self.chroma_client.delete_collection(name=collection_name)
        except ValueError:
            pass  # Colección no existe, continuar

        # Crear colección nueva
        self.collection = self.chroma_client.create_collection(
            name=collection_name
        )

        print(f"✅ Module 2 OptimizedRAG inicializado")
        print(f"   - Cache habilitado: {self.use_cache}")
        print(f"   - Re-ranking habilitado: {self.use_reranking}")
        print(f"   - Chunk overlap: {self.chunk_overlap}")

    def create_chunks(self, text: str) -> List[str]:
        """
        Crear chunks CON overlap (mejora del Módulo 1)
        """
        chunks = []

        # Calcular step size basado en overlap
        step_size = self.chunk_size - self.chunk_overlap

        # Crear chunks con overlap
        for i in range(0, len(text) - self.chunk_size + 1, step_size):
            chunk = text[i:i + self.chunk_size]

            # Solo añadir chunks significativos
            if len(chunk.strip()) > 50:
                chunks.append(chunk)

        # Añadir último chunk si es necesario
        if len(text) % step_size > 50:
            chunks.append(text[-(self.chunk_size):])

        self.chunks = chunks

        print(
            f"✂️ Creados {len(chunks)} chunks de {self.chunk_size} chars con {self.chunk_overlap} overlap")

        # Análisis de overlap
        overlaps = len(chunks) - len(text) // self.chunk_size
        print(f"   - Chunks adicionales por overlap: {overlaps}")
        print(f"   - Cobertura mejorada: +{(overlaps/len(chunks)*100):.1f}%")

        return chunks

    def smart_chunking(self, text: str) -> List[Dict[str, Any]]:
        """
        Chunking inteligente que respeta límites de párrafos y frases
        """
        chunks_with_metadata = []
        paragraphs = text.split('\n\n')

        current_chunk = ""
        current_section = ""
        chunk_index = 0

        for para_idx, paragraph in enumerate(paragraphs):
            # Detectar secciones (líneas en mayúsculas)
            if paragraph.isupper() and len(paragraph) < 100:
                current_section = paragraph.strip()
                continue

            # Si el párrafo cabe en el chunk actual
            if len(current_chunk) + len(paragraph) < self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                # Guardar chunk actual si existe
                if current_chunk:
                    chunks_with_metadata.append({
                        "text": current_chunk.strip(),
                        "metadata": {
                            "chunk_index": chunk_index,
                            "section": current_section,
                            "paragraph_start": para_idx - 1,
                            "type": "smart_chunk"
                        }
                    })
                    chunk_index += 1

                # Empezar nuevo chunk con overlap
                if self.chunk_overlap > 0 and current_chunk:
                    # Tomar últimas N palabras del chunk anterior
                    words = current_chunk.split()
                    # Aproximadamente
                    overlap_words = words[-(self.chunk_overlap//10):]
                    current_chunk = " ".join(
                        overlap_words) + "\n\n" + paragraph + "\n\n"
                else:
                    current_chunk = paragraph + "\n\n"

        # Añadir último chunk
        if current_chunk:
            chunks_with_metadata.append({
                "text": current_chunk.strip(),
                "metadata": {
                    "chunk_index": chunk_index,
                    "section": current_section,
                    "paragraph_start": para_idx,
                    "type": "smart_chunk"
                }
            })

        return chunks_with_metadata

    @measure_performance
    def index_chunks(self, chunks: List[str] = None):
        """Indexar con metadatos enriquecidos"""
        if chunks is None:
            chunks = self.chunks

        if not chunks:
            raise ValueError("No hay chunks para indexar")

        print(
            f"🔢 Indexando {len(chunks)} chunks con metadatos enriquecidos...")

        # Preparar metadatos enriquecidos
        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            # Detectar información clave en el chunk
            has_numbers = any(char.isdigit() for char in chunk)
            has_policy = "política" in chunk.lower() or "policy" in chunk.lower()
            has_benefits = "beneficio" in chunk.lower() or "benefit" in chunk.lower()

            ids.append(f"chunk_{i}_v2")
            documents.append(chunk)
            metadatas.append({
                "chunk_index": i,
                "module": "2",
                "timestamp": time.time(),
                "length": len(chunk),
                "has_numbers": has_numbers,
                "has_policy": has_policy,
                "has_benefits": has_benefits,
                "overlap_start": i > 0,  # Si tiene overlap con anterior
                # Si tiene overlap con siguiente
                "overlap_end": i < len(chunks) - 1
            })

        # Indexar en ChromaDB
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

        self.indexed = True
        print(f"✅ {len(chunks)} chunks indexados con metadatos enriquecidos")

    def search_with_rerank(self, query: str, k: int = None) -> Dict[str, Any]:
        """Búsqueda con re-ranking basado en relevancia"""
        if k is None:
            k = self.config.retrieval_params[self.module]["top_k"]

        # Buscar más resultados para re-rankear
        initial_k = k * 2

        # Búsqueda inicial
        results = self.collection.query(
            query_texts=[query],
            n_results=initial_k
        )

        if not results['documents'][0]:
            return {"documents": [], "distances": [], "scores": []}

        # Re-ranking basado en múltiples factores
        documents = results['documents'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0] if 'metadatas' in results else []

        # Calcular scores para re-ranking
        reranked = []
        for i, (doc, dist, meta) in enumerate(zip(documents, distances, metadatas)):
            # Score base (inverso de la distancia)
            base_score = 1.0 / (1.0 + dist)

            # Bonus por metadatos relevantes
            metadata_bonus = 0
            if meta:
                if query_has_numbers(query) and meta.get('has_numbers'):
                    metadata_bonus += 0.1
                if 'política' in query.lower() and meta.get('has_policy'):
                    metadata_bonus += 0.15
                if 'beneficio' in query.lower() and meta.get('has_benefits'):
                    metadata_bonus += 0.15

            # Bonus por longitud (chunks más largos suelen ser más informativos)
            length_bonus = min(0.1, len(doc) / 10000)

            # Score final
            final_score = base_score + metadata_bonus + length_bonus

            reranked.append({
                'document': doc,
                'distance': dist,
                'metadata': meta,
                'score': final_score
            })

        # Ordenar por score final
        reranked.sort(key=lambda x: x['score'], reverse=True)

        # Tomar top K
        top_results = reranked[:k]

        return {
            "documents": [r['document'] for r in top_results],
            "distances": [r['distance'] for r in top_results],
            "scores": [r['score'] for r in top_results],
            "metadatas": [r['metadata'] for r in top_results]
        }

    def generate_response(self, query: str, context: str) -> str:
        """Generar respuesta con prompt optimizado"""

        # Prompt mejorado del Módulo 2
        prompt = f"""
        Eres un asistente experto en recursos humanos analizando documentos oficiales de la empresa.
        
        CONTEXTO RELEVANTE:
        {context}
        
        PREGUNTA DEL EMPLEADO:
        {query}
        
        INSTRUCCIONES:
        1. Responde ÚNICAMENTE basándote en el contexto proporcionado
        2. Si la información está incompleta, indícalo claramente
        3. Usa bullet points para listas cuando sea apropiado
        4. Sé específico con números, fechas y políticas
        5. Mantén un tono profesional pero amigable
        6. Si no tienes la información, di: "No encuentro esa información en los documentos disponibles"
        
        RESPUESTA:
        """

        # Generar respuesta con temperatura optimizada
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=250  # Un poco más que módulo 1
        )

        return response.choices[0].message.content

    def query(self, question: str, k: int = None) -> Dict[str, Any]:
        """
        Pipeline RAG optimizado con cache y re-ranking
        """
        print(f"\n{'='*50}")
        print(f"📝 Query: {question}")
        print(f"{'='*50}")

        # Check cache primero
        cache_key = hashlib.md5(f"{question}_{k}".encode()).hexdigest()

        if self.use_cache:
            cached_result = self.query_cache.get(cache_key)
            if cached_result:
                print("⚡ Respuesta desde CACHE")
                # Añadir flag de cache
                cached_result['from_cache'] = True
                # Tiempo simbólico
                cached_result['metrics']['total_time_ms'] = 5
                return cached_result

        start_time = time.time()

        # 1. Retrieval con re-ranking
        search_start = time.time()
        if self.use_reranking:
            search_results = self.search_with_rerank(question, k)
            print(f"🎯 Usando re-ranking")
        else:
            search_results = self.search(question, k)
        search_time = (time.time() - search_start) * 1000

        # 2. Preparar contexto
        context = "\n\n---\n\n".join(search_results["documents"])

        # 3. Generación
        gen_start = time.time()
        response = self.generate_response(question, context)
        gen_time = (time.time() - gen_start) * 1000

        # Métricas
        total_time = (time.time() - start_time) * 1000

        # Estimar costos (con prompt optimizado)
        input_tokens = len(context.split()) + \
            len(question.split()) + 50  # +50 por prompt
        output_tokens = len(response.split())
        cost = (input_tokens * 0.0015 + output_tokens * 0.002) / 1000

        # Registrar en métricas globales
        self.metrics_tracker.log_query(
            module=self.module,
            query=question,
            response=response,
            latency=total_time,
            cost=cost,
            tokens=input_tokens + output_tokens
        )

        # Resultado completo
        result = {
            "query": question,
            "response": response,
            "chunks_used": len(search_results["documents"]),
            "context_length": len(context),
            "from_cache": False,
            "used_reranking": self.use_reranking,
            "metrics": {
                "retrieval_time_ms": search_time,
                "generation_time_ms": gen_time,
                "total_time_ms": total_time,
                "estimated_cost_usd": cost,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }
        }

        # Guardar en cache
        if self.use_cache:
            self.query_cache.put(cache_key, result)

        # Imprimir resumen
        print(f"\n📊 Métricas Optimizadas:")
        print(f"   - Retrieval: {search_time:.0f}ms")
        print(f"   - Generation: {gen_time:.0f}ms")
        print(f"   - Total: {total_time:.0f}ms")
        print(f"   - Costo: ${cost:.4f}")
        print(f"   - Re-ranking: {'Sí' if self.use_reranking else 'No'}")
        print(f"\n💬 Respuesta:")
        print(f"   {response[:200]}...")

        return result

    def clear_cache(self):
        """Limpiar todos los caches"""
        self.query_cache.clear()
        self.embedding_cache.clear()
        print("🗑️ Cache limpiado")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        return {
            "query_cache_size": len(self.query_cache.cache),
            "query_cache_capacity": self.query_cache.capacity,
            "embedding_cache_size": len(self.embedding_cache.cache),
            "embedding_cache_capacity": self.embedding_cache.capacity,
            "cache_hit_rate": "N/A"  # Requeriría tracking adicional
        }


def query_has_numbers(query: str) -> bool:
    """Helper: verificar si la query contiene números"""
    return any(char.isdigit() for char in query)
