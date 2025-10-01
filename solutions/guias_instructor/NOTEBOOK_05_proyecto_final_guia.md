# Soluciones Proyecto Final (Notebook 05) - NIVEL 2 WORKSHOP

## 📋 Estructura del Módulo 5

El notebook 05 es el proyecto final donde los participantes:
1. Eligen un caso de uso (Support, Technical Docs, Business Intelligence, o custom)
2. Personalizan la clase base `MyCustomRAG`
3. Implementan features específicas de su dominio
4. Prueban y presentan su sistema

## ✅ Estado Actual (Post-Corrección)

### Cambios Realizados:
1. ✅ **Transformado de template vacío a clase base funcional**
2. ✅ **Hereda de Module2_OptimizedRAG** (toda la funcionalidad básica incluida)
3. ✅ **Métodos funcionales** con TODOs claramente marcados
4. ✅ **Ejemplos de uso** para diferentes tipos de datos
5. ✅ **Sistema de testing** con hints por dominio

### Filosofía del Módulo 5:
- **90% autonomía**: Los participantes deciden qué construir
- **Base funcional**: La clase padre ya funciona, solo personalizan
- **TODOs opcionales**: Cada método tiene implementación básica + TODOs para mejorar
- **Flexibilidad total**: Pueden elegir qué métodos extender

## 🎯 Casos de Uso Propuestos

### Opción A: Customer Support Bot
**Objetivo**: Responder queries de soporte automáticamente

**Datos sugeridos**:
- FAQs (JSON)
- Tickets históricos (CSV)
- Knowledge base (PDF)

**Features especiales**:
- Auto-escalación a humano si confidence < 70%
- Categorización automática de tickets
- Historial de conversación

**Métricas clave**:
- Tiempo de primera respuesta
- % de resolución automática
- Satisfacción del cliente

---

### Opción B: Technical Documentation Assistant
**Objetivo**: Ayudar a developers con documentación técnica

**Datos sugeridos**:
- API docs (Markdown)
- Code samples (archivos .py, .js)
- READMEs (Markdown)

**Features especiales**:
- Generación de código
- Versionado de docs
- Detección de deprecated APIs

**Métricas clave**:
- Precisión técnica
- Código generado funcional
- Coverage de API

---

### Opción B: Business Intelligence RAG
**Objetivo**: Insights de negocio desde datos

**Datos sugeridos**:
- Reports (PDF)
- KPIs (CSV)
- Dashboard exports (JSON)

**Features especiales**:
- Visualizaciones automáticas
- Detección de tendencias
- Alertas de anomalías

**Métricas clave**:
- Insights accionables
- Precisión de predicciones
- Tiempo de análisis

---

### Opción D: Custom (Tu idea)
**Objetivo**: Lo que necesites

**Ejemplos reales**:
- Legal document search
- Medical literature review
- E-commerce product recommendations
- HR policy assistant
- Sales enablement tool

---

## 💻 Implementación Completa: Ejemplo "Customer Support Bot"

```python
# ============= CUSTOMER SUPPORT BOT =============

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent / 'src'))

from module_2_optimized import Module2_OptimizedRAG
import json
import pandas as pd
import time

class CustomerSupportRAG(Module2_OptimizedRAG):
    """
    Sistema RAG especializado en soporte al cliente

    Features:
    - Auto-escalación basada en confianza
    - Categorización de tickets
    - Historial de conversación
    - Métricas de satisfacción
    """

    def __init__(self):
        super().__init__()
        self.name = "Customer Support Bot"
        self.version = "1.0.0"

        # Config específica de soporte
        self.config = {
            "domain": "customer_support",
            "language": "es",
            "tone": "friendly_professional",
            "escalation_threshold": 0.7,
            "max_context_tickets": 5
        }

        # Componentes especiales
        self.ticket_categories = [
            "account", "billing", "technical",
            "shipping", "product", "other"
        ]
        self.conversation_history = []
        self.escalated_queries = []

        print(f"✅ {self.name} v{self.version} inicializado")
        print(f"   Umbral de escalación: {self.config['escalation_threshold']}")

    def load_support_data(self):
        """Cargar datos de soporte (FAQs + tickets)"""
        print("📥 Cargando datos de soporte...")

        # 1. Cargar FAQs desde JSON
        faqs_path = "../data/faqs.json"
        with open(faqs_path) as f:
            faqs = json.load(f)

        # Convertir FAQs a texto para indexar
        faq_texts = []
        for faq in faqs:
            text = f"Q: {faq['question']}\nA: {faq['answer']}\nCategoría: {faq['category']}"
            faq_texts.append(text)

        print(f"   ✅ {len(faq_texts)} FAQs cargadas")

        # 2. Cargar tickets históricos desde CSV
        tickets_path = "../data/support_tickets.csv"
        df = pd.read_csv(tickets_path)

        # Convertir tickets a texto
        ticket_texts = []
        for _, ticket in df.iterrows():
            text = f"Ticket #{ticket['ticket_id']}: {ticket['description']}\nResolución: {ticket['resolution']}"
            ticket_texts.append(text)

        print(f"   ✅ {len(ticket_texts)} tickets históricos cargados")

        # 3. Combinar y crear chunks
        all_texts = "\n\n---\n\n".join(faq_texts + ticket_texts)
        chunks = self.create_chunks(all_texts, chunk_size=800, chunk_overlap=150)

        # 4. Indexar
        self.index_chunks(chunks)

        print(f"   ✅ {len(chunks)} chunks indexados")

        return {
            "faqs": len(faq_texts),
            "tickets": len(ticket_texts),
            "chunks": len(chunks)
        }

    def categorize_query(self, query: str) -> str:
        """Categorizar query automáticamente"""
        query_lower = query.lower()

        # Reglas simples de categorización
        if any(word in query_lower for word in ['cuenta', 'password', 'login', 'acceso']):
            return "account"
        elif any(word in query_lower for word in ['pago', 'factura', 'cobro', 'billing']):
            return "billing"
        elif any(word in query_lower for word in ['error', 'bug', 'no funciona', 'técnico']):
            return "technical"
        elif any(word in query_lower for word in ['envío', 'entrega', 'shipping']):
            return "shipping"
        elif any(word in query_lower for word in ['producto', 'feature', 'funcionalidad']):
            return "product"
        else:
            return "other"

    def calculate_confidence(self, result: dict) -> float:
        """
        Calcular score de confianza basado en:
        - Número de sources
        - Similaridad de sources
        - Longitud de respuesta
        """
        num_sources = result['metrics'].get('num_sources', 0)

        # Score base por número de sources
        if num_sources >= 3:
            confidence = 0.9
        elif num_sources == 2:
            confidence = 0.75
        elif num_sources == 1:
            confidence = 0.6
        else:
            confidence = 0.3

        # Ajustar por longitud de respuesta
        answer_length = len(result.get('response', ''))
        if answer_length < 50:
            confidence *= 0.8
        elif answer_length > 200:
            confidence = min(confidence * 1.1, 1.0)

        return round(confidence, 2)

    def support_query(self, question: str, user_id: str = "anonymous"):
        """
        Query principal con features de soporte
        """
        print(f"\n💬 Support Query de {user_id}")
        print(f"   Q: {question}")

        start_time = time.time()

        # 1. Categorizar
        category = self.categorize_query(question)
        print(f"   📂 Categoría: {category}")

        # 2. Query base
        result = self.query(question)

        # 3. Calcular confianza
        confidence = self.calculate_confidence(result)
        print(f"   🎯 Confianza: {confidence:.0%}")

        # 4. Decidir escalación
        should_escalate = confidence < self.config['escalation_threshold']

        if should_escalate:
            print(f"   ⚠️  Escalando a agente humano (confianza < {self.config['escalation_threshold']:.0%})")
            self.escalated_queries.append({
                "question": question,
                "confidence": confidence,
                "category": category,
                "timestamp": time.time()
            })

        # 5. Construir respuesta mejorada
        enhanced_response = {
            "answer": result['response'],
            "category": category,
            "confidence": confidence,
            "escalated": should_escalate,
            "sources": result['metrics']['num_sources'],
            "latency_ms": (time.time() - start_time) * 1000,
            "user_id": user_id
        }

        # 6. Guardar en historial
        self.conversation_history.append({
            "user_id": user_id,
            "question": question,
            "category": category,
            "confidence": confidence,
            "escalated": should_escalate,
            "timestamp": time.time()
        })

        return enhanced_response

    def get_support_stats(self):
        """Estadísticas del sistema de soporte"""
        total_queries = len(self.conversation_history)
        escalated = len([q for q in self.conversation_history if q['escalated']])

        if total_queries == 0:
            return {"message": "No hay queries todavía"}

        # Calcular métricas
        auto_resolution_rate = ((total_queries - escalated) / total_queries) * 100
        avg_confidence = sum(q['confidence'] for q in self.conversation_history) / total_queries

        # Por categoría
        category_counts = {}
        for q in self.conversation_history:
            cat = q['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        return {
            "total_queries": total_queries,
            "auto_resolved": total_queries - escalated,
            "escalated": escalated,
            "auto_resolution_rate": f"{auto_resolution_rate:.1f}%",
            "avg_confidence": f"{avg_confidence:.0%}",
            "queries_by_category": category_counts,
            "top_category": max(category_counts, key=category_counts.get) if category_counts else None
        }

# ============= DEMO =============

# Crear instancia
support_bot = CustomerSupportRAG()

# Cargar datos
stats = support_bot.load_support_data()
print(f"\n📊 Datos cargados: {stats}")

# Queries de prueba
test_queries = [
    ("¿Cómo reseteo mi contraseña?", "user_001"),
    ("¿Cuándo llega mi pedido?", "user_002"),
    ("Error al procesar pago", "user_003"),
    ("¿Qué features tiene el plan premium?", "user_001"),
]

print("\n" + "="*60)
print("🧪 TESTING CUSTOMER SUPPORT BOT")
print("="*60)

for question, user_id in test_queries:
    result = support_bot.support_query(question, user_id)

    print(f"\n📝 Respuesta:")
    print(f"   {result['answer'][:150]}...")
    print(f"   Categoría: {result['category']} | Confianza: {result['confidence']:.0%}")
    print(f"   Escalado: {'Sí' if result['escalated'] else 'No'} | Latencia: {result['latency_ms']:.0f}ms")
    print("-"*60)
    time.sleep(1)

# Mostrar estadísticas
print("\n📊 ESTADÍSTICAS DEL SISTEMA")
print("="*60)
stats = support_bot.get_support_stats()
for key, value in stats.items():
    print(f"{key}: {value}")

print("\n✅ Customer Support Bot Demo Completo!")
```

---

## 💻 Implementación Completa: Ejemplo "Technical Docs Assistant"

```python
# ============= TECHNICAL DOCUMENTATION ASSISTANT =============

from module_2_optimized import Module2_OptimizedRAG
import re
from typing import List, Dict

class TechnicalDocsRAG(Module2_OptimizedRAG):
    """
    Sistema RAG para documentación técnica

    Features:
    - Detección de código en queries
    - Generación de ejemplos de código
    - Versionado de APIs
    - Links a documentación oficial
    """

    def __init__(self):
        super().__init__()
        self.name = "Technical Docs Assistant"
        self.version = "1.0.0"

        self.config = {
            "domain": "technical_documentation",
            "language": "es",
            "code_languages": ["python", "javascript", "bash"],
            "api_version": "v1.0",
            "include_code_examples": True
        }

        # Cache de código generado
        self.code_cache = {}

        print(f"✅ {self.name} v{self.version} inicializado")

    def load_technical_docs(self):
        """Cargar documentación técnica"""
        print("📥 Cargando documentación técnica...")

        # Cargar PDF técnico
        doc = self.load_document("../data/technical_docs.pdf")
        chunks = self.create_chunks(doc, chunk_size=1200, chunk_overlap=200)
        self.index_chunks(chunks)

        print(f"   ✅ {len(chunks)} chunks técnicos indexados")
        return len(chunks)

    def detect_code_request(self, query: str) -> bool:
        """Detectar si piden código"""
        code_keywords = [
            'ejemplo', 'código', 'code', 'sample',
            'cómo usar', 'implementar', 'función'
        ]
        return any(kw in query.lower() for kw in code_keywords)

    def extract_api_name(self, query: str) -> str:
        """Extraer nombre de API/función de la query"""
        # Buscar patrones comunes: authenticate(), /api/users, class Database
        patterns = [
            r'(\w+)\(\)',  # function()
            r'/api/(\w+)',  # /api/endpoint
            r'class (\w+)'  # class Name
        ]

        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(1)

        return None

    def generate_code_example(self, api_name: str, language: str = "python") -> str:
        """Generar ejemplo de código (simplificado)"""

        # Templates básicos
        templates = {
            "authenticate": '''
```python
from api import authenticate

# Autenticar usuario
result = authenticate(
    username="user@example.com",
    password="secure_password"
)

if result.success:
    print(f"Token: {result.token}")
else:
    print(f"Error: {result.error}")
```
''',
            "users": '''
```python
import requests

# Obtener lista de usuarios
response = requests.get(
    "https://api.example.com/users",
    headers={"Authorization": f"Bearer {token}"}
)

users = response.json()
for user in users:
    print(f"{user['name']} - {user['email']}")
```
''',
            "Database": '''
```python
from database import Database

# Conectar a base de datos
db = Database(
    host="localhost",
    port=5432,
    database="myapp",
    user="admin"
)

# Ejecutar query
results = db.query("SELECT * FROM users WHERE active = true")
db.close()
```
'''
        }

        return templates.get(api_name, f"# Ejemplo de código para {api_name} no disponible")

    def technical_query(self, question: str):
        """Query con features técnicas"""
        print(f"\n🔧 Technical Query: {question}")

        # 1. Detectar si piden código
        wants_code = self.detect_code_request(question)

        # 2. Query base
        result = self.query(question)

        # 3. Si piden código, generarlo
        code_example = None
        if wants_code:
            api_name = self.extract_api_name(question)
            if api_name:
                code_example = self.generate_code_example(api_name)
                print(f"   💻 Código generado para: {api_name}")

        # 4. Construir respuesta mejorada
        enhanced_response = result['response']

        if code_example:
            enhanced_response += f"\n\n### Ejemplo de Código:\n{code_example}"

        # Añadir link a docs
        enhanced_response += f"\n\n📚 [Ver documentación oficial](https://docs.ejemplo.com)"

        return {
            "answer": enhanced_response,
            "code_included": code_example is not None,
            "api_detected": self.extract_api_name(question),
            "sources": result['metrics']['num_sources']
        }

# ============= DEMO =============

tech_docs = TechnicalDocsRAG()
tech_docs.load_technical_docs()

# Test
queries = [
    "¿Cómo funciona la función authenticate()?",
    "¿Qué es un sistema RAG?",
    "Dame un ejemplo de uso de /api/users"
]

for q in queries:
    result = tech_docs.technical_query(q)
    print(f"\nRespuesta:\n{result['answer'][:300]}...")
    print(f"Código incluido: {result['code_included']}")
    print("-"*60)
```

---

## 🎯 Guía para Participantes

### Para completar el proyecto final exitosamente:

#### 1. Elegir Caso de Uso (5 min)
```python
# Pregúntate:
# - ¿Qué problema quiero resolver?
# - ¿Qué datos tengo disponibles?
# - ¿Qué hace único a mi solución?
```

#### 2. Personalizar la Clase Base (15 min)
```python
class MiRAG(Module2_OptimizedRAG):
    def __init__(self):
        super().__init__()
        self.name = "MI NOMBRE ÚNICO"
        self.config = {
            # MIS parámetros específicos
        }
```

#### 3. Implementar Método de Carga (10 min)
```python
def load_my_data(self):
    # Cargar MIS datos (PDF/JSON/CSV/API)
    # Procesarlos para MI dominio
    # Indexarlos
    pass
```

#### 4. Añadir Feature Especial (10 min)
```python
def my_special_feature(self, query):
    # LO QUE HACE ÚNICO a mi sistema
    # Ejemplos: escalación, código, visualización
    pass
```

#### 5. Probar y Iterar (10 min)
```python
# Probar con queries REALES de MI dominio
# Medir latencia, calidad, costo
# Iterar hasta que funcione bien
```

---

## ✅ Checklist de Completitud

Para considerar el proyecto final completo:

- [ ] Caso de uso claramente definido
- [ ] Clase personalizada con nombre único
- [ ] Configuración adaptada al dominio
- [ ] Al menos un método de carga de datos implementado
- [ ] Al menos una feature especial funcional
- [ ] 3-5 queries de prueba exitosas
- [ ] Métricas básicas medidas
- [ ] Presentación de 5 min preparada

---

## 🎤 Template de Presentación

```
SLIDE 1: TÍTULO (30 seg)
- Nombre del proyecto
- Problema que resuelve
- Tu nombre

SLIDE 2: DEMO (2 min)
- Ejecutar 2-3 queries en vivo
- Mostrar respuestas
- Destacar features especiales

SLIDE 3: ARQUITECTURA (1 min)
- Diagrama simple
- Componentes clave
- Lo que hace único

SLIDE 4: MÉTRICAS (1 min)
- Latencia lograda
- Calidad/Accuracy
- Impacto estimado

SLIDE 5: PRÓXIMOS PASOS (30 seg)
- Qué mejorarías
- Cómo lo llevarías a producción
- Visión a futuro
```

---

**🎉 El proyecto final es TU oportunidad de brillar. No hay respuestas correctas o incorrectas, solo soluciones creativas a problemas reales!**
