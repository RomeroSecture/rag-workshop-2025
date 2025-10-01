# EJERCICIO 1: Optimizar chunk size - NIVEL 3 PRODUCCIÓN
# Solución production-ready con análisis estadístico, visualización y CI/CD

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent.parent / 'src'))

from module_2_optimized import Module2_OptimizedRAG
from shared_config import TestSuite, Module
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import json
from datetime import datetime

class ChunkSizeOptimizer:
    """
    Optimizador production-ready para encontrar el chunk_size óptimo.

    Features:
    - Múltiples iteraciones para estabilidad estadística
    - Análisis de varianza y percentiles
    - Visualización de trade-offs
    - Exportación de resultados
    - Recomendaciones basadas en SLAs
    """

    def __init__(self, num_iterations: int = 3):
        self.num_iterations = num_iterations
        self.results = []

    def optimize(
        self,
        chunk_sizes: List[int],
        test_queries: List[str],
        max_chunks: int = 20,
        target_latency_ms: float = 1000.0,
        min_quality_score: float = 0.75
    ) -> Dict:
        """
        Ejecuta optimización completa de chunk_size.

        Args:
            chunk_sizes: Tamaños a probar
            test_queries: Queries de evaluación
            max_chunks: Máximo de chunks a indexar
            target_latency_ms: SLA de latencia objetivo
            min_quality_score: Calidad mínima aceptable

        Returns:
            Dict con resultados y recomendaciones
        """
        print(f"🔬 OPTIMIZADOR DE CHUNK SIZE (Production Mode)")
        print(f"   Iteraciones: {self.num_iterations}")
        print(f"   Chunk sizes: {chunk_sizes}")
        print(f"   Test queries: {len(test_queries)}")
        print(f"   Target latency: {target_latency_ms}ms")
        print(f"   Min quality: {min_quality_score}")
        print("=" * 70)

        for size in chunk_sizes:
            print(f"\n🔧 Evaluando chunk_size={size}")

            size_results = {
                'chunk_size': size,
                'iterations': [],
                'latencies': [],
                'qualities': [],
                'num_chunks': 0
            }

            # Múltiples iteraciones para estabilidad
            for iteration in range(self.num_iterations):
                print(f"   Iteración {iteration + 1}/{self.num_iterations}...", end=' ')

                try:
                    # Crear instancia fresca
                    rag = Module2_OptimizedRAG()
                    rag.chunk_size = size

                    # Cargar y procesar
                    doc = rag.load_document()
                    chunks = rag.create_chunks(doc)
                    rag.index_chunks(chunks[:max_chunks])

                    if iteration == 0:
                        size_results['num_chunks'] = len(chunks)

                    # Evaluar queries
                    iteration_latencies = []
                    iteration_qualities = []

                    for query in test_queries:
                        start = time.time()
                        response = rag.query(query)
                        elapsed = (time.time() - start) * 1000
                        iteration_latencies.append(elapsed)

                        eval_result = TestSuite.evaluate_response(
                            response['response'],
                            Module.OPTIMIZED
                        )
                        iteration_qualities.append(eval_result['score'])

                        time.sleep(0.3)  # Rate limiting

                    # Guardar resultados de iteración
                    size_results['latencies'].extend(iteration_latencies)
                    size_results['qualities'].extend(iteration_qualities)

                    print(f"✓ (avg: {np.mean(iteration_latencies):.0f}ms)")

                except Exception as e:
                    print(f"✗ Error: {e}")
                    continue

            # Calcular estadísticas agregadas
            if size_results['latencies']:
                size_results['stats'] = {
                    'latency_mean': np.mean(size_results['latencies']),
                    'latency_median': np.median(size_results['latencies']),
                    'latency_p95': np.percentile(size_results['latencies'], 95),
                    'latency_std': np.std(size_results['latencies']),
                    'quality_mean': np.mean(size_results['qualities']),
                    'quality_median': np.median(size_results['qualities']),
                    'quality_std': np.std(size_results['qualities']),
                    'combined_score': np.mean(size_results['qualities']) / (np.mean(size_results['latencies']) / 1000)
                }

                self.results.append(size_results)

                print(f"   📊 Latencia: {size_results['stats']['latency_mean']:.0f}ms "
                      f"(p95: {size_results['stats']['latency_p95']:.0f}ms, "
                      f"σ: {size_results['stats']['latency_std']:.0f}ms)")
                print(f"   🎯 Calidad: {size_results['stats']['quality_mean']:.3f} "
                      f"(σ: {size_results['stats']['quality_std']:.3f})")

        # Generar recomendaciones
        recommendations = self._generate_recommendations(
            target_latency_ms,
            min_quality_score
        )

        return {
            'results': self.results,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

    def _generate_recommendations(
        self,
        target_latency_ms: float,
        min_quality_score: float
    ) -> Dict:
        """Genera recomendaciones basadas en SLAs"""

        # Encontrar mejores configuraciones
        valid_configs = [
            r for r in self.results
            if r['stats']['quality_mean'] >= min_quality_score
        ]

        if not valid_configs:
            return {
                'status': 'error',
                'message': f'Ninguna configuración alcanzó calidad mínima de {min_quality_score}'
            }

        # Configuración más balanceada
        best_balanced = max(valid_configs, key=lambda x: x['stats']['combined_score'])

        # Más rápida que cumple SLA
        fast_configs = [
            r for r in valid_configs
            if r['stats']['latency_mean'] <= target_latency_ms
        ]
        best_fast = min(fast_configs, key=lambda x: x['stats']['latency_mean']) if fast_configs else None

        # Mejor calidad
        best_quality = max(valid_configs, key=lambda x: x['stats']['quality_mean'])

        return {
            'status': 'success',
            'balanced': {
                'chunk_size': best_balanced['chunk_size'],
                'latency_ms': round(best_balanced['stats']['latency_mean'], 0),
                'quality': round(best_balanced['stats']['quality_mean'], 3),
                'meets_sla': best_balanced['stats']['latency_mean'] <= target_latency_ms
            },
            'fastest': {
                'chunk_size': best_fast['chunk_size'] if best_fast else None,
                'latency_ms': round(best_fast['stats']['latency_mean'], 0) if best_fast else None,
                'quality': round(best_fast['stats']['quality_mean'], 3) if best_fast else None
            } if best_fast else None,
            'highest_quality': {
                'chunk_size': best_quality['chunk_size'],
                'latency_ms': round(best_quality['stats']['latency_mean'], 0),
                'quality': round(best_quality['stats']['quality_mean'], 3),
                'meets_sla': best_quality['stats']['latency_mean'] <= target_latency_ms
            }
        }

    def visualize(self, save_path: str = None):
        """Genera visualizaciones comprehensivas"""

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        chunk_sizes = [r['chunk_size'] for r in self.results]
        latency_means = [r['stats']['latency_mean'] for r in self.results]
        latency_p95s = [r['stats']['latency_p95'] for r in self.results]
        quality_means = [r['stats']['quality_mean'] for r in self.results]
        combined_scores = [r['stats']['combined_score'] for r in self.results]

        # Gráfico 1: Latencia (mean + p95)
        ax1 = axes[0, 0]
        ax1.plot(chunk_sizes, latency_means, marker='o', label='Mean', linewidth=2)
        ax1.plot(chunk_sizes, latency_p95s, marker='s', label='p95', linewidth=2, linestyle='--')
        ax1.axhline(y=1000, color='r', linestyle=':', label='Target SLA (1000ms)')
        ax1.set_xlabel('Chunk Size')
        ax1.set_ylabel('Latency (ms)')
        ax1.set_title('⏱️ Latencia por Chunk Size')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Gráfico 2: Calidad
        ax2 = axes[0, 1]
        ax2.plot(chunk_sizes, quality_means, marker='o', color='green', linewidth=2)
        ax2.axhline(y=0.75, color='r', linestyle=':', label='Min Quality (0.75)')
        ax2.set_xlabel('Chunk Size')
        ax2.set_ylabel('Quality Score')
        ax2.set_title('🎯 Calidad por Chunk Size')
        ax2.set_ylim(0, 1.0)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Gráfico 3: Trade-off Latencia vs Calidad
        ax3 = axes[1, 0]
        scatter = ax3.scatter(latency_means, quality_means, s=200, c=chunk_sizes,
                             cmap='viridis', alpha=0.7, edgecolors='black', linewidth=2)

        for i, size in enumerate(chunk_sizes):
            ax3.annotate(f'{size}', (latency_means[i], quality_means[i]),
                        ha='center', va='center', fontweight='bold')

        ax3.set_xlabel('Latency (ms)')
        ax3.set_ylabel('Quality Score')
        ax3.set_title('📊 Trade-off: Latencia vs Calidad')
        ax3.axhline(y=0.75, color='r', linestyle=':', alpha=0.5)
        ax3.axvline(x=1000, color='r', linestyle=':', alpha=0.5)
        ax3.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax3, label='Chunk Size')

        # Gráfico 4: Combined Score
        ax4 = axes[1, 1]
        bars = ax4.bar(chunk_sizes, combined_scores, color='skyblue', edgecolor='black', linewidth=2)

        # Destacar el mejor
        best_idx = combined_scores.index(max(combined_scores))
        bars[best_idx].set_color('gold')
        bars[best_idx].set_edgecolor('red')
        bars[best_idx].set_linewidth(3)

        ax4.set_xlabel('Chunk Size')
        ax4.set_ylabel('Combined Score (Quality/Latency)')
        ax4.set_title('🏆 Score Combinado (Mayor es Mejor)')
        ax4.grid(True, alpha=0.3, axis='y')

        for i, v in enumerate(combined_scores):
            ax4.text(chunk_sizes[i], v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')

        plt.suptitle('🔬 Análisis de Optimización de Chunk Size', fontsize=16, y=1.00)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Visualización guardada en: {save_path}")

        plt.show()

    def export_results(self, output_path: str):
        """Exporta resultados a JSON y CSV"""

        # JSON completo
        json_path = output_path.replace('.csv', '.json')
        with open(json_path, 'w') as f:
            json.dump({
                'results': self.results,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)

        print(f"💾 Resultados JSON guardados en: {json_path}")

        # CSV para análisis
        df_data = []
        for r in self.results:
            df_data.append({
                'chunk_size': r['chunk_size'],
                'num_chunks': r['num_chunks'],
                'latency_mean_ms': round(r['stats']['latency_mean'], 2),
                'latency_median_ms': round(r['stats']['latency_median'], 2),
                'latency_p95_ms': round(r['stats']['latency_p95'], 2),
                'latency_std_ms': round(r['stats']['latency_std'], 2),
                'quality_mean': round(r['stats']['quality_mean'], 3),
                'quality_std': round(r['stats']['quality_std'], 3),
                'combined_score': round(r['stats']['combined_score'], 3)
            })

        df = pd.DataFrame(df_data)
        df.to_csv(output_path, index=False)
        print(f"📊 Resultados CSV guardados en: {output_path}")


# =============== EJECUCIÓN ===============

if __name__ == "__main__":
    # Configuración
    CHUNK_SIZES = [300, 500, 800, 1000, 1500]
    TEST_QUERIES = [
        "¿Cuál es la política de vacaciones?",
        "¿Qué beneficios tienen los empleados senior?",
        "¿Cómo funciona el trabajo remoto?",
        "¿Cuál es el proceso de onboarding?",
        "¿Qué días festivos tiene la empresa?"
    ]

    # Ejecutar optimización
    optimizer = ChunkSizeOptimizer(num_iterations=3)

    results = optimizer.optimize(
        chunk_sizes=CHUNK_SIZES,
        test_queries=TEST_QUERIES,
        max_chunks=20,
        target_latency_ms=1000.0,
        min_quality_score=0.75
    )

    # Mostrar recomendaciones
    print("\n" + "=" * 70)
    print("🎯 RECOMENDACIONES FINALES")
    print("=" * 70)

    rec = results['recommendations']

    if rec['status'] == 'success':
        print(f"\n🏆 CONFIGURACIÓN BALANCEADA (Recomendada):")
        print(f"   Chunk Size: {rec['balanced']['chunk_size']}")
        print(f"   Latencia: {rec['balanced']['latency_ms']}ms")
        print(f"   Calidad: {rec['balanced']['quality']}")
        print(f"   Cumple SLA: {'✅' if rec['balanced']['meets_sla'] else '❌'}")

        if rec['fastest']:
            print(f"\n⚡ CONFIGURACIÓN RÁPIDA:")
            print(f"   Chunk Size: {rec['fastest']['chunk_size']}")
            print(f"   Latencia: {rec['fastest']['latency_ms']}ms")
            print(f"   Calidad: {rec['fastest']['quality']}")

        print(f"\n🎯 CONFIGURACIÓN DE MÁXIMA CALIDAD:")
        print(f"   Chunk Size: {rec['highest_quality']['chunk_size']}")
        print(f"   Latencia: {rec['highest_quality']['latency_ms']}ms")
        print(f"   Calidad: {rec['highest_quality']['quality']}")
        print(f"   Cumple SLA: {'✅' if rec['highest_quality']['meets_sla'] else '❌'}")

    # Visualizar
    optimizer.visualize(save_path='chunk_size_optimization.png')

    # Exportar
    optimizer.export_results('chunk_size_optimization_results.csv')

    print("\n✅ Optimización completada!")
