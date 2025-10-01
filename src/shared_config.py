"""
Configuración Maestra del Workshop RAG
Este archivo mantiene la coherencia entre todos los módulos
"""

import os
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import time
from datetime import datetime
from enum import Enum

class Module(Enum):
    """Módulos del workshop"""
    BASICS = 1
    OPTIMIZED = 2
    ADVANCED = 3
    PRODUCTION = 4

@dataclass
class RAGMasterConfig:
    """Configuración que evoluciona pero mantiene coherencia"""
    
    # CONSTANTES (nunca cambian durante el workshop)
    BASE_DOCUMENT = "data/company_handbook.pdf"
    VECTOR_DB = "chromadb"
    COLLECTION_NAME = "rag_workshop_2025"
    API_VERSION = "v1"
    
    # MODELOS (evolucionan por módulo)
    embedding_models = {
        Module.BASICS: "text-embedding-3-small",
        Module.OPTIMIZED: "text-embedding-3-small",
        Module.ADVANCED: "text-embedding-3-small",
        Module.PRODUCTION: "text-embedding-3-small"
    }
    
    llm_models = {
        Module.BASICS: "gpt-3.5-turbo",
        Module.OPTIMIZED: "gpt-3.5-turbo",
        Module.ADVANCED: "gpt-3.5-turbo",
        Module.PRODUCTION: {
            "simple": "gpt-3.5-turbo",
            "complex": "gpt-4",
            "fallback": "gpt-3.5-turbo"
        }
    }
    
    # CHUNKING PARAMETERS (evolucionan)
    chunking_params = {
        Module.BASICS: {"size": 1000, "overlap": 0, "strategy": "fixed"},
        Module.OPTIMIZED: {"size": 1000, "overlap": 200, "strategy": "recursive"},
        Module.ADVANCED: {"size": 1000, "overlap": 200, "strategy": "semantic"},
        Module.PRODUCTION: {"size": 800, "overlap": 200, "strategy": "adaptive"}
    }
    
    # RETRIEVAL PARAMETERS
    retrieval_params = {
        Module.BASICS: {"top_k": 3, "threshold": 0.0},
        Module.OPTIMIZED: {"top_k": 5, "threshold": 0.7},
        Module.ADVANCED: {"top_k": 5, "threshold": 0.75, "rerank": True},
        Module.PRODUCTION: {"top_k": 10, "threshold": 0.8, "rerank": True, "mmr": True}
    }
    
    # DOCUMENTOS (se añaden progresivamente)
    documents = {
        Module.BASICS: ["company_handbook.pdf"],
        Module.OPTIMIZED: ["company_handbook.pdf", "technical_docs.pdf"],
        Module.ADVANCED: ["company_handbook.pdf", "technical_docs.pdf", "faqs.json"],
        Module.PRODUCTION: ["company_handbook.pdf", "technical_docs.pdf", "faqs.json", "support_tickets.csv"]
    }
    
    # MÉTRICAS TARGET
    target_metrics = {
        Module.BASICS: {"latency": 2000, "cost": 0.01, "accuracy": 0.7},
        Module.OPTIMIZED: {"latency": 1000, "cost": 0.008, "accuracy": 0.8},
        Module.ADVANCED: {"latency": 800, "cost": 0.006, "accuracy": 0.85},
        Module.PRODUCTION: {"latency": 500, "cost": 0.004, "accuracy": 0.9}
    }

class TestSuite:
    """Queries consistentes para toda la formación"""
    
    # Query héroe - La usamos TODO el día
    HERO_QUERY = "¿Cuál es la política de vacaciones?"
    
    # Evolución de respuestas esperadas
    EXPECTED_EVOLUTION = {
        Module.BASICS: "22 días al año",
        Module.OPTIMIZED: "22 días base, 25 con 5+ años, 30 con 10+ años",
        Module.ADVANCED: "22 días base, aumenta con antigüedad. Fuente: Handbook p.47",
        Module.PRODUCTION: "[CACHED] 22 días base, detalles completos..."
    }
    
    # Set de queries para diferentes propósitos
    QUERIES = {
        "simple": [
            "¿Cuál es la política de vacaciones?",
            "¿Cuál es el horario de trabajo?",
            "¿Hay trabajo remoto?"
        ],
        "complex": [
            "¿Cómo se comparan nuestras vacaciones con el estándar del sector?",
            "¿Qué beneficios tienen los seniors con 5 años de antigüedad?",
            "¿Cuál es el proceso completo de onboarding?"
        ],
        "edge_cases": [
            "¿Qué pasa si trabajo en festivos?",
            "¿Puedo combinar vacaciones con excedencia?",
            "¿Hay políticas especiales para padres/madres?"
        ],
        "multilingual": [
            "What is the vacation policy?",
            "Qual è la politica delle vacanze?",
            "Quelle est la politique de vacances?"
        ]
    }
    
    @staticmethod
    def evaluate_response(response: str, module: Module) -> Dict[str, Any]:
        """Evaluar si la respuesta cumple las expectativas del módulo"""
        expected = TestSuite.EXPECTED_EVOLUTION[module]
        
        # Métricas de evaluación
        has_basic_info = "22 días" in response
        has_seniority_info = "5 años" in response or "antigüedad" in response
        has_source = "Fuente:" in response or "página" in response
        is_cached = "[CACHED]" in response
        
        score = 0.0
        if module == Module.BASICS:
            score = 1.0 if has_basic_info else 0.0
        elif module == Module.OPTIMIZED:
            score = 0.5 if has_basic_info else 0.0
            score += 0.5 if has_seniority_info else 0.0
        elif module == Module.ADVANCED:
            score = 0.3 if has_basic_info else 0.0
            score += 0.3 if has_seniority_info else 0.0
            score += 0.4 if has_source else 0.0
        elif module == Module.PRODUCTION:
            score = 0.9 if is_cached else 0.7
            score += 0.1 if has_source else 0.0
        
        return {
            "score": score,
            "passed": score >= 0.7,
            "has_basic_info": has_basic_info,
            "has_seniority_info": has_seniority_info,
            "has_source": has_source,
            "is_cached": is_cached,
            "expected": expected,
            "actual": response[:100] + "..." if len(response) > 100 else response
        }

class MetricsTracker:
    """Tracker global de métricas durante el workshop"""
    
    def __init__(self):
        self.metrics = {
            Module.BASICS: [],
            Module.OPTIMIZED: [],
            Module.ADVANCED: [],
            Module.PRODUCTION: []
        }
        self.start_time = datetime.now()
        
    def log_query(self, module: Module, query: str, response: str, 
                  latency: float, cost: float, tokens: int):
        """Registrar métricas de una query"""
        self.metrics[module].append({
            "timestamp": datetime.now(),
            "query": query,
            "response": response[:200],
            "latency_ms": latency,
            "cost_usd": cost,
            "tokens": tokens,
            "module": module.name
        })
        
    def get_summary(self) -> Dict[str, Any]:
        """Obtener resumen de métricas"""
        summary = {}
        for module, metrics_list in self.metrics.items():
            if metrics_list:
                latencies = [m["latency_ms"] for m in metrics_list]
                costs = [m["cost_usd"] for m in metrics_list]
                tokens = [m["tokens"] for m in metrics_list]
                
                summary[module.name] = {
                    "queries_count": len(metrics_list),
                    "avg_latency_ms": sum(latencies) / len(latencies),
                    "total_cost_usd": sum(costs),
                    "total_tokens": sum(tokens),
                    "improvement_from_baseline": None
                }
                
                # Calcular mejora respecto al baseline
                if module != Module.BASICS and Module.BASICS in self.metrics and self.metrics[Module.BASICS]:
                    baseline_latency = summary[Module.BASICS.name]["avg_latency_ms"]
                    current_latency = summary[module.name]["avg_latency_ms"]
                    improvement = (baseline_latency - current_latency) / baseline_latency * 100
                    summary[module.name]["improvement_from_baseline"] = f"{improvement:.1f}%"
        
        return summary
    
    def plot_progress(self):
        """Generar gráfico de progreso (para notebooks)"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            # Preparar datos
            data = []
            for module, metrics_list in self.metrics.items():
                for metric in metrics_list:
                    data.append({
                        "Module": module.name,
                        "Latency": metric["latency_ms"],
                        "Cost": metric["cost_usd"] * 1000  # Convertir a milicents
                    })
            
            if not data:
                print("No hay datos para graficar")
                return
                
            df = pd.DataFrame(data)
            
            # Crear gráfico
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Latency por módulo
            df.boxplot(column="Latency", by="Module", ax=ax1)
            ax1.set_title("Latencia por Módulo")
            ax1.set_ylabel("Latencia (ms)")
            ax1.set_xlabel("Módulo")
            
            # Cost por módulo
            df.boxplot(column="Cost", by="Module", ax=ax2)
            ax2.set_title("Costo por Módulo")
            ax2.set_ylabel("Costo (millicents)")
            ax2.set_xlabel("Módulo")
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Matplotlib no disponible. Mostrando resumen textual:")
            print(self.get_summary())

# Instancia global para todo el workshop
GLOBAL_METRICS = MetricsTracker()
GLOBAL_CONFIG = RAGMasterConfig()

# Funciones de utilidad
def get_api_key(service: str = "openai") -> str:
    """Obtener API key del ambiente"""
    key_mapping = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "cohere": "COHERE_API_KEY",
        "huggingface": "HUGGINGFACE_TOKEN"
    }
    
    env_var = key_mapping.get(service)
    if not env_var:
        raise ValueError(f"Servicio no soportado: {service}")
    
    key = os.getenv(env_var)
    if not key:
        raise ValueError(f"Por favor configura {env_var} en tu archivo .env")
    
    return key

def measure_performance(func):
    """Decorador para medir performance"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        latency = (end - start) * 1000  # ms
        
        # Log si es una función de query
        if hasattr(func, "__self__") and hasattr(func.__self__, "module"):
            print(f"⏱️ {func.__name__}: {latency:.0f}ms")
        
        return result, latency
    return wrapper

# Configuración de logging
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("rag_workshop")