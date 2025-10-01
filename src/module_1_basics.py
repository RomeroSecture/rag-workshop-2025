"""
Módulo 1: RAG Básico
Este es el código base que será extendido en módulos posteriores
"""

import os
import time
from typing import List, Dict, Optional, Any
import numpy as np
from openai import OpenAI
import chromadb
from PyPDF2 import PdfReader
from shared_config import RAGMasterConfig, TestSuite, MetricsTracker, Module, measure_performance


class Module1_BasicRAG:
    """
    Versión 1: RAG más simple posible
    Esta clase será EXTENDIDA en módulos posteriores
    """

    def __init__(self):
        """Inicializar con configuración del módulo"""
        self.module = Module.BASICS
        self.config = RAGMasterConfig()

        # Configuración específica del módulo
        self.chunk_size = self.config.chunking_params[self.module]["size"]
        self.chunk_overlap = self.config.chunking_params[self.module]["overlap"]
        self.model = self.config.llm_models[self.module]
        self.embedding_model = self.config.embedding_models[self.module]

        # Clientes
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chroma_client = chromadb.Client()

        # Crear colección única para el workshop
        collection_name = f"{self.config.COLLECTION_NAME}_module1"
        try:
            self.collection = self.chroma_client.create_collection(
                collection_name)
        except:
            self.chroma_client.delete_collection(name=collection_name)
            self.collection = self.chroma_client.create_collection(
                collection_name)

        # Tracker de métricas
        self.metrics_tracker = MetricsTracker()

        # Estado
        self.documents_loaded = []
        self.chunks = []
        self.indexed = False

        print(f"✅ Module 1 BasicRAG inicializado")
        print(f"   - Modelo: {self.model}")
        print(f"   - Chunk size: {self.chunk_size}")
        print(f"   - Chunk overlap: {self.chunk_overlap}")

    def load_document(self, filepath: str = None) -> str:
        """Cargar documento de prueba"""
        if filepath is None:
            filepath = f"data/{self.config.documents[self.module][0]}"

        print(f"📄 Cargando documento: {filepath}")

        try:
            if filepath.endswith('.pdf'):
                with open(filepath, 'rb') as file:
                    pdf_reader = PdfReader(file)
                    text = ""
                    for page_num, page in enumerate(pdf_reader.pages):
                        text += f"\n--- Página {page_num + 1} ---\n"
                        text += page.extract_text()
            else:
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()

            self.documents_loaded.append(filepath)
            print(f"✅ Documento cargado: {len(text)} caracteres")
            return text

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {filepath}")
            print("Creando documento de ejemplo...")
            self._create_sample_document(filepath)
            return self.load_document(filepath)

    def create_chunks(self, text: str) -> List[str]:
        """
        Crear chunks simples sin overlap (Módulo 1)
        Será mejorado en módulos posteriores
        """
        chunks = []

        # Chunking simple: división fija sin overlap
        for i in range(0, len(text), self.chunk_size):
            chunk = text[i:i + self.chunk_size]
            if len(chunk.strip()) > 50:  # Ignorar chunks muy pequeños
                chunks.append(chunk)

        self.chunks = chunks
        print(
            f"✂️ Creados {len(chunks)} chunks de {self.chunk_size} caracteres (sin overlap)")

        # Estadísticas
        chunk_lengths = [len(c) for c in chunks]
        print(f"   - Promedio: {np.mean(chunk_lengths):.0f} chars")
        print(f"   - Min: {min(chunk_lengths)} chars")
        print(f"   - Max: {max(chunk_lengths)} chars")

        return chunks

    @measure_performance
    def index_chunks(self, chunks: List[str] = None):
        """Indexar chunks en ChromaDB"""
        if chunks is None:
            chunks = self.chunks

        if not chunks:
            raise ValueError("No hay chunks para indexar")

        print(f"🔢 Indexando {len(chunks)} chunks...")

        # Preparar IDs y metadatos
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "chunk_index": i,
                "module": "1",
                "timestamp": time.time()
            }
            for i in range(len(chunks))
        ]

        # Indexar en ChromaDB
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

        self.indexed = True
        print(f"✅ {len(chunks)} chunks indexados exitosamente")

    @measure_performance
    def search(self, query: str, k: int = None) -> Dict[str, Any]:
        """Buscar chunks relevantes"""
        if not self.indexed:
            raise ValueError(
                "No hay documentos indexados. Ejecuta index_chunks() primero")

        if k is None:
            k = self.config.retrieval_params[self.module]["top_k"]

        print(f"🔍 Buscando {k} chunks relevantes para: '{query[:50]}...'")

        # Buscar en ChromaDB
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        # Procesar resultados
        documents = results['documents'][0] if results['documents'] else []
        distances = results['distances'][0] if results['distances'] else []

        print(f"✅ Encontrados {len(documents)} chunks relevantes")

        return {
            "documents": documents,
            "distances": distances,
            "metadatas": results.get('metadatas', [[]])[0]
        }

    def generate_response(self, query: str, context: str) -> str:
        """Generar respuesta usando el LLM"""
        # Prompt simple para Módulo 1
        prompt = f"""
        Contexto:
        {context}
        
        Pregunta: {query}
        
        Instrucciones: Responde basándote ÚNICAMENTE en el contexto proporcionado.
        Si no encuentras la información en el contexto, di "No tengo esa información en el contexto proporcionado".
        Sé conciso y directo.
        """

        # Generar respuesta
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )

        return response.choices[0].message.content

    def query(self, question: str, k: int = None) -> Dict[str, Any]:
        """
        Pipeline RAG completo: search + generate
        Retorna diccionario con respuesta y métricas
        """
        print(f"\n{'='*50}")
        print(f"📝 Query: {question}")
        print(f"{'='*50}")

        start_time = time.time()

        # 1. Retrieval
        search_start = time.time()
        search_results = self.search(question, k)
        search_time = (time.time() - search_start) * 1000

        # 2. Preparar contexto
        context = "\n\n".join(search_results["documents"])

        # 3. Generación
        gen_start = time.time()
        response = self.generate_response(question, context)
        gen_time = (time.time() - gen_start) * 1000

        # Métricas
        total_time = (time.time() - start_time) * 1000

        # Estimar costos (aproximado)
        input_tokens = len(context.split()) + len(question.split())
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
            "metrics": {
                "retrieval_time_ms": search_time,
                "generation_time_ms": gen_time,
                "total_time_ms": total_time,
                "estimated_cost_usd": cost,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }
        }

        # Imprimir resumen
        print(f"\n📊 Métricas:")
        print(f"   - Retrieval: {search_time:.0f}ms")
        print(f"   - Generation: {gen_time:.0f}ms")
        print(f"   - Total: {total_time:.0f}ms")
        print(f"   - Costo estimado: ${cost:.4f}")
        print(f"\n💬 Respuesta:")
        print(f"   {response[:200]}...")

        return result

    def run_test_suite(self) -> Dict[str, Any]:
        """Ejecutar suite de pruebas del módulo"""
        print(f"\n🧪 Ejecutando Test Suite - Módulo 1")
        print("=" * 50)

        results = []

        # Probar con diferentes tipos de queries
        for query_type, queries in TestSuite.QUERIES.items():
            if query_type in ["simple", "complex"]:  # Solo algunos para módulo 1
                for query in queries[:2]:  # Limitar a 2 por tipo
                    print(f"\n📝 Probando: {query}")
                    result = self.query(query)

                    # Evaluar respuesta
                    evaluation = TestSuite.evaluate_response(
                        result["response"],
                        self.module
                    )

                    results.append({
                        "query": query,
                        "type": query_type,
                        "passed": evaluation["passed"],
                        "score": evaluation["score"],
                        "latency": result["metrics"]["total_time_ms"],
                        "cost": result["metrics"]["estimated_cost_usd"]
                    })

                    time.sleep(1)  # Rate limiting

        # Resumen
        import pandas as pd
        df = pd.DataFrame(results)

        print(f"\n📈 RESUMEN TEST SUITE - MÓDULO 1")
        print("=" * 50)
        print(f"Total queries: {len(results)}")
        print(f"Passed: {df['passed'].sum()}/{len(results)}")
        print(f"Score promedio: {df['score'].mean():.2f}")
        print(f"Latencia promedio: {df['latency'].mean():.0f}ms")
        print(f"Costo total: ${df['cost'].sum():.4f}")

        return {
            "results": results,
            "summary": {
                "total": len(results),
                "passed": df['passed'].sum(),
                "avg_score": df['score'].mean(),
                "avg_latency": df['latency'].mean(),
                "total_cost": df['cost'].sum()
            }
        }

    def _create_sample_document(self, filepath: str):
        """Crear documento de ejemplo si no existe"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        sample_content = """
        MANUAL DEL EMPLEADO - TECH CORP 2025
        
        POLÍTICA DE VACACIONES:
        Los empleados tienen derecho a 22 días hábiles de vacaciones al año.
        Empleados con 5+ años: 25 días hábiles.
        Empleados con 10+ años: 30 días hábiles.
        
        HORARIO DE TRABAJO:
        Horario estándar: 9:00 - 18:00 (Lunes a Viernes)
        Horario flexible disponible con aprobación del manager.
        
        TRABAJO REMOTO:
        Modelo híbrido: 2-3 días en oficina por semana.
        Trabajo remoto completo disponible para roles específicos.
        
        BENEFICIOS:
        - Seguro médico premium
        - Plan de pensiones
        - Gimnasio en oficina
        - Formación continua
        - Stock options
        """

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sample_content)

        print(f"✅ Documento de ejemplo creado: {filepath}")
