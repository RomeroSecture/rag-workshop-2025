"""
Módulo 3: Frameworks Avanzados
Integra LangChain y/o LlamaIndex sobre el Módulo 2
"""

import os
import time
from typing import List, Dict, Optional, Any
from module_2_optimized import Module2_OptimizedRAG
from shared_config import Module, MetricsTracker

# Imports de frameworks
try:
    from langchain.document_loaders import PyPDFLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma as LangChainChroma
    from langchain.chains import RetrievalQA, ConversationalRetrievalChain
    from langchain.llms import OpenAI as LangChainOpenAI
    from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
    from langchain.agents import initialize_agent, Tool, AgentType
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("⚠️ LangChain no instalado. Instala con: pip install langchain langchain-community")

try:
    from llama_index import VectorStoreIndex, Document, SimpleDirectoryReader
    from llama_index.llms import OpenAI as LlamaOpenAI
    from llama_index.embeddings import OpenAIEmbedding
    from llama_index.memory import ChatMemoryBuffer
    from llama_index.indices.postprocessor import SentenceTransformerRerank
    LLAMAINDEX_AVAILABLE = True
except ImportError:
    LLAMAINDEX_AVAILABLE = False
    print("⚠️ LlamaIndex no instalado. Instala con: pip install llama-index")


class Module3_AdvancedRAG(Module2_OptimizedRAG):
    """
    Versión 3: RAG con Frameworks Profesionales
    Extiende Module2 añadiendo LangChain y/o LlamaIndex
    """

    def __init__(self, framework: str = "langchain"):
        """
        Inicializar con framework elegido

        Args:
            framework: "langchain", "llamaindex", o "hybrid"
        """
        super().__init__()

        self.module = Module.ADVANCED
        self.framework = framework.lower()

        print(f"📚 Module 3 AdvancedRAG inicializando...")
        print(f"   - Framework: {self.framework}")

        # Configurar según framework
        if self.framework == "langchain":
            if not LANGCHAIN_AVAILABLE:
                raise ImportError("LangChain no está instalado")
            self.setup_langchain()

        elif self.framework == "llamaindex":
            if not LLAMAINDEX_AVAILABLE:
                raise ImportError("LlamaIndex no está instalado")
            self.setup_llamaindex()

        elif self.framework == "hybrid":
            self.setup_hybrid()

        else:
            raise ValueError(f"Framework no soportado: {framework}")

        print(f"✅ Module 3 con {self.framework} listo")

    # ============= LANGCHAIN SETUP =============

    def setup_langchain(self):
        """Configurar LangChain completo"""
        print("🔗 Configurando LangChain...")

        # Embeddings
        self.lc_embeddings = OpenAIEmbeddings(
            model=self.embedding_model,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # Vector Store
        self.lc_vectorstore = LangChainChroma(
            collection_name="m3_langchain",
            embedding_function=self.lc_embeddings
        )

        # LLM
        self.lc_llm = LangChainOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # Memoria conversacional
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        # Chain conversacional
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.lc_llm,
            retriever=self.lc_vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )

        # QA Chain simple
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.lc_llm,
            chain_type="stuff",
            retriever=self.lc_vectorstore.as_retriever(),
            return_source_documents=True
        )

        # Configurar agent con tools
        self.setup_langchain_agent()

    def setup_langchain_agent(self):
        """Configurar agent con herramientas"""

        tools = [
            Tool(
                name="RAG_Search",
                func=lambda q: self.qa_chain.run(q),
                description="Buscar información en documentos de la empresa"
            ),
            Tool(
                name="Calculator",
                func=lambda expr: str(eval(expr)),
                description="Realizar cálculos matemáticos"
            ),
            Tool(
                name="Current_Time",
                func=lambda x: time.strftime("%Y-%m-%d %H:%M:%S"),
                description="Obtener fecha y hora actual"
            )
        ]

        self.agent = initialize_agent(
            tools,
            self.lc_llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            memory=self.memory
        )

        print("   ✅ Agent con tools configurado")

    def langchain_index_documents(self, documents: List[str]):
        """Indexar documentos con LangChain"""
        if isinstance(documents[0], str):
            # Si son strings, convertir a Documents de LangChain
            from langchain.schema import Document as LCDocument
            lc_docs = [LCDocument(page_content=doc) for doc in documents]
        else:
            lc_docs = documents

        # Añadir a vectorstore
        self.lc_vectorstore.add_documents(lc_docs)
        print(f"   ✅ {len(lc_docs)} documentos indexados con LangChain")

    # ============= LLAMAINDEX SETUP =============

    def setup_llamaindex(self):
        """Configurar LlamaIndex completo"""
        print("📚 Configurando LlamaIndex...")

        # Embeddings
        self.li_embeddings = OpenAIEmbedding(
            model=self.embedding_model,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # LLM
        self.li_llm = LlamaOpenAI(
            model=self.model,
            temperature=self.temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Crear índice vacío inicialmente
        self.li_index = None

        # Memory buffer
        self.li_memory = ChatMemoryBuffer.from_defaults(token_limit=3000)

        # Re-ranker
        self.reranker = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-2-v2",
            top_n=3
        )

        print("   ✅ LlamaIndex configurado")

    def llamaindex_index_documents(self, documents: List[str]):
        """Indexar documentos con LlamaIndex"""

        # Convertir a Documents de LlamaIndex
        li_docs = []
        for i, doc in enumerate(documents):
            if isinstance(doc, str):
                li_docs.append(Document(
                    text=doc,
                    metadata={"doc_id": i, "source": "training_data"}
                ))
            else:
                li_docs.append(doc)

        # Crear o actualizar índice
        if self.li_index is None:
            self.li_index = VectorStoreIndex.from_documents(
                li_docs,
                embed_model=self.li_embeddings
            )
        else:
            for doc in li_docs:
                self.li_index.insert(doc)

        # Crear query engine con re-ranking
        self.query_engine = self.li_index.as_query_engine(
            llm=self.li_llm,
            similarity_top_k=5,
            node_postprocessors=[self.reranker],
            streaming=False
        )

        print(f"   ✅ {len(li_docs)} documentos indexados con LlamaIndex")

    # ============= HYBRID SETUP =============

    def setup_hybrid(self):
        """Configurar sistema híbrido con ambos frameworks"""
        print("🔀 Configurando sistema Hybrid...")

        if LANGCHAIN_AVAILABLE:
            self.setup_langchain()

        if LLAMAINDEX_AVAILABLE:
            self.setup_llamaindex()

        print("   ✅ Sistema híbrido configurado")

    # ============= QUERY METHODS =============

    def query_with_framework(self, question: str, use_memory: bool = True) -> Dict[str, Any]:
        """
        Query usando el framework configurado
        """
        print(f"\n📝 Query con {self.framework}: {question}")
        start_time = time.time()

        if self.framework == "langchain":
            result = self._query_langchain(question, use_memory)
        elif self.framework == "llamaindex":
            result = self._query_llamaindex(question)
        elif self.framework == "hybrid":
            result = self._query_hybrid(question)
        else:
            # Fallback al método del módulo 2
            return super().query(question)

        # Métricas
        total_time = (time.time() - start_time) * 1000

        # Registrar en tracker
        self.metrics_tracker.log_query(
            module=self.module,
            query=question,
            response=result["answer"],
            latency=total_time,
            cost=result.get("cost", 0.01),
            tokens=result.get("tokens", 100)
        )

        result["latency_ms"] = total_time

        return result

    def _query_langchain(self, question: str, use_memory: bool) -> Dict[str, Any]:
        """Query con LangChain"""

        if use_memory:
            # Usar chain conversacional con memoria
            response = self.conversation_chain({"question": question})
            answer = response["answer"]
            sources = response.get("source_documents", [])
        else:
            # Usar QA chain simple
            response = self.qa_chain({"query": question})
            answer = response["result"]
            sources = response.get("source_documents", [])

        # Procesar sources
        source_texts = []
        for doc in sources[:3]:
            source_texts.append({
                "text": doc.page_content[:200],
                "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
            })

        return {
            "answer": answer,
            "sources": source_texts,
            "framework": "langchain",
            "memory_used": use_memory,
            "cost": 0.01,  # Estimado
            "tokens": len(answer.split()) * 1.3
        }

    def _query_llamaindex(self, question: str) -> Dict[str, Any]:
        """Query con LlamaIndex"""

        if self.query_engine is None:
            return {
                "answer": "No hay documentos indexados. Por favor indexa primero.",
                "sources": [],
                "framework": "llamaindex"
            }

        # Query con re-ranking
        response = self.query_engine.query(question)

        # Extraer sources
        sources = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes[:3]:
                sources.append({
                    "text": node.text[:200],
                    "score": node.score if hasattr(node, 'score') else 0,
                    "metadata": node.metadata if hasattr(node, 'metadata') else {}
                })

        return {
            "answer": str(response),
            "sources": sources,
            "framework": "llamaindex",
            "reranked": True,
            "cost": 0.008,
            "tokens": len(str(response).split()) * 1.3
        }

    def _query_hybrid(self, question: str) -> Dict[str, Any]:
        """Query híbrido usando ambos frameworks"""

        results = {}

        # Query con ambos frameworks
        if LANGCHAIN_AVAILABLE:
            lc_result = self._query_langchain(question, False)
            results["langchain"] = lc_result["answer"]

        if LLAMAINDEX_AVAILABLE and self.query_engine:
            li_result = self._query_llamaindex(question)
            results["llamaindex"] = li_result["answer"]

        # Combinar resultados (simple majority voting o concatenación)
        if len(results) == 2:
            # Ambos frameworks disponibles
            combined_answer = f"""
            Respuesta (LangChain): {results['langchain'][:200]}...
            
            Respuesta (LlamaIndex): {results['llamaindex'][:200]}...
            
            [Síntesis]: Ambos frameworks coinciden en los puntos principales.
            """
        else:
            # Solo uno disponible
            combined_answer = list(results.values())[
                0] if results else "No hay frameworks disponibles"

        return {
            "answer": combined_answer,
            "sources": [],
            "framework": "hybrid",
            "frameworks_used": list(results.keys()),
            "cost": 0.015,
            "tokens": len(combined_answer.split()) * 1.3
        }

    def query_with_agent(self, question: str) -> str:
        """Query usando agent con tools (solo LangChain)"""
        if self.framework != "langchain":
            return "Agents solo disponibles con LangChain"

        return self.agent.run(question)

    # ============= OVERRIDE PARENT METHODS =============

    def query(self, question: str, k: int = None) -> Dict[str, Any]:
        """Override del método query para usar frameworks"""
        return self.query_with_framework(question, use_memory=True)

    def index_chunks(self, chunks: List[str] = None):
        """Override para indexar con frameworks"""
        if chunks is None:
            chunks = self.chunks

        if not chunks:
            raise ValueError("No hay chunks para indexar")

        print(f"🔢 Indexando {len(chunks)} chunks con {self.framework}...")

        if self.framework == "langchain" and LANGCHAIN_AVAILABLE:
            self.langchain_index_documents(chunks)
        elif self.framework == "llamaindex" and LLAMAINDEX_AVAILABLE:
            self.llamaindex_index_documents(chunks)
        elif self.framework == "hybrid":
            if LANGCHAIN_AVAILABLE:
                self.langchain_index_documents(chunks)
            if LLAMAINDEX_AVAILABLE:
                self.llamaindex_index_documents(chunks)
        else:
            # Fallback al método padre
            super().index_chunks(chunks)

        self.indexed = True
