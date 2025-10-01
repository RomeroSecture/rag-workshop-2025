"""
Utilidades para el RAG Workshop 2025
Incluye generación de datos de ejemplo y funciones helper
"""

import os
import json
import csv
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def create_sample_pdf(filename: str, title: str, content: str):
    """Crear un PDF de ejemplo"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Título
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, height - 100, title)
        
        # Contenido
        c.setFont("Helvetica", 12)
        y = height - 150
        
        # Dividir el contenido en líneas
        lines = content.split('\n')
        for line in lines:
            if y < 100:  # Nueva página si es necesario
                c.showPage()
                y = height - 100
                c.setFont("Helvetica", 12)
            
            # Manejar líneas largas
            if len(line) > 80:
                wrapped = simpleSplit(line, "Helvetica", 12, width - 200)
                for wrap in wrapped:
                    c.drawString(100, y, wrap)
                    y -= 20
            else:
                c.drawString(100, y, line)
                y -= 20
        
        c.save()
        print(f"✅ Creado: {filename}")
        
    except ImportError:
        # Fallback a archivo de texto si no está reportlab
        with open(filename.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
            f.write(f"{title}\n{'='*50}\n\n{content}")
        print(f"⚠️ PDF no disponible, creado TXT: {filename.replace('.pdf', '.txt')}")

def create_sample_data():
    """Generar todos los datos de ejemplo para el workshop"""
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 1. Company Handbook
    handbook_content = """
MANUAL DEL EMPLEADO - TECH CORP 2025

CAPÍTULO 1: BIENVENIDA
Bienvenido a Tech Corp, donde la innovación y el bienestar de nuestros empleados son nuestra prioridad.

CAPÍTULO 2: HORARIO DE TRABAJO
- Horario estándar: 9:00 - 18:00 (Lunes a Viernes)
- Horario flexible: Entre 7:00 - 10:00 entrada, 8 horas diarias
- Viernes cortos: Salida a las 15:00 en verano (Junio-Septiembre)

CAPÍTULO 3: POLÍTICA DE VACACIONES
Nuestro sistema de vacaciones recompensa la lealtad y experiencia:

Empleados nuevos (0-5 años): 22 días hábiles al año
Empleados senior (5-10 años): 25 días hábiles al año
Empleados veteran (10+ años): 30 días hábiles al año

Beneficios adicionales:
- Día de cumpleaños libre
- 2 días de asuntos propios
- Posibilidad de comprar hasta 5 días adicionales
- Acumulación máxima: 40 días

CAPÍTULO 4: TRABAJO REMOTO
Tech Corp adopta un modelo híbrido flexible:
- Mínimo 2 días en oficina por semana
- Trabajo remoto completo: Previa aprobación del manager
- Equipamiento para home office proporcionado
- Compensación internet: 50€/mes

CAPÍTULO 5: BENEFICIOS
- Seguro médico premium (empleado + familia)
- Plan de pensiones: Empresa aporta 5% del salario
- Gimnasio en oficina o compensación 40€/mes
- Formación continua: 2000€/año
- Stock options para empleados 2+ años

CAPÍTULO 6: DESARROLLO PROFESIONAL
- Evaluaciones trimestrales
- Plan de carrera personalizado
- Mentoring program
- Rotación entre equipos disponible
- Conferencias: 2 al año pagadas

CAPÍTULO 7: CÓDIGO DE CONDUCTA
- Respeto y diversidad
- Tolerancia cero al acoso
- Confidencialidad de información
- Uso responsable de recursos
- Canal de denuncias anónimo

CAPÍTULO 8: PROCESO DE ONBOARDING
Semana 1: Orientación y setup
Semana 2-4: Formación específica del rol
Mes 2-3: Proyecto de ramping con mentor
Mes 3: Evaluación y feedback

CAPÍTULO 9: COMPENSACIÓN
- Revisión salarial anual
- Bonus por objetivos: hasta 20% del salario
- Referral bonus: 2000€
- Aumentos por promoción: mínimo 15%

CAPÍTULO 10: POLÍTICAS ESPECIALES
- Baja parental: 16 semanas pagadas
- Cuidado de familiares: 5 días al año
- Mudanza: 2 días libres
- Matrimonio: 15 días naturales
    """
    
    create_sample_pdf(
        str(data_dir / "company_handbook.pdf"),
        "Manual del Empleado 2025",
        handbook_content
    )
    
    # 2. Technical Documentation
    tech_docs_content = """
DOCUMENTACIÓN TÉCNICA - ARQUITECTURA DE SISTEMAS

1. ARQUITECTURA DE MICROSERVICIOS

1.1 Servicios Core:
- Auth Service: Maneja autenticación y autorización (Node.js)
- User Service: Gestión de usuarios y perfiles (Python/FastAPI)
- Payment Service: Procesamiento de pagos (Java/Spring)
- Notification Service: Email, SMS, Push (Go)
- Analytics Service: Métricas y reporting (Python/Pandas)

1.2 Stack Tecnológico:
- Frontend: React 18, TypeScript, Next.js
- Backend: Python 3.11, FastAPI, SQLAlchemy
- Base de Datos: PostgreSQL 15, Redis, MongoDB
- Message Queue: RabbitMQ, Apache Kafka
- Containerización: Docker, Kubernetes
- CI/CD: GitLab CI, ArgoCD
- Monitoring: Prometheus, Grafana, ELK Stack

2. ESTÁNDARES DE DESARROLLO

2.1 Código:
- Python: PEP 8, Black formatter
- JavaScript: ESLint, Prettier
- Git Flow: feature/, bugfix/, hotfix/
- Code Review obligatorio: mínimo 2 aprobaciones
- Coverage mínimo: 80%

2.2 APIs:
- RESTful design
- Versionado: /api/v1/, /api/v2/
- Autenticación: OAuth 2.0, JWT
- Rate Limiting: 1000 req/hour
- Documentación: OpenAPI 3.0

3. SEGURIDAD

3.1 Mejores Prácticas:
- Encriptación: AES-256 en reposo, TLS 1.3 en tránsito
- Secrets Management: HashiCorp Vault
- Vulnerability Scanning: Semanal con Snyk
- Penetration Testing: Trimestral
- OWASP Top 10 compliance

3.2 Backup y Disaster Recovery:
- Backups: Diarios, retención 30 días
- RPO: 1 hora
- RTO: 4 horas
- Multi-region deployment

4. PERFORMANCE

4.1 SLAs:
- Uptime: 99.95%
- Response time p95: <200ms
- Error rate: <0.1%

4.2 Optimización:
- Caching: Redis, CDN (CloudFlare)
- Database: Índices, query optimization
- Lazy loading, code splitting
- Image optimization: WebP, lazy loading

5. DEPLOYMENT

5.1 Environments:
- Development: dev.techcorp.internal
- Staging: staging.techcorp.internal
- Production: api.techcorp.com

5.2 Release Process:
- Feature Flags: LaunchDarkly
- Blue-Green Deployment
- Canary Releases: 5% → 25% → 50% → 100%
- Rollback automático si error rate >1%
    """
    
    create_sample_pdf(
        str(data_dir / "technical_docs.pdf"),
        "Documentación Técnica",
        tech_docs_content
    )
    
    # 3. FAQs JSON
    faqs = {
        "faqs": [
            {
                "id": 1,
                "category": "Vacaciones",
                "question": "¿Puedo transferir días de vacaciones al siguiente año?",
                "answer": "Sí, puedes transferir hasta 5 días de vacaciones no utilizados al siguiente año. Deben ser usados antes del 31 de marzo.",
                "views": 1523,
                "helpful": 89
            },
            {
                "id": 2,
                "category": "Trabajo Remoto",
                "question": "¿Necesito estar disponible en horario de oficina cuando trabajo desde casa?",
                "answer": "Sí, debes estar disponible durante el horario core (10:00-16:00). Fuera de ese horario, tienes flexibilidad siempre que cumplas tus 8 horas diarias.",
                "views": 2341,
                "helpful": 156
            },
            {
                "id": 3,
                "category": "Beneficios",
                "question": "¿Cómo solicito el reembolso del gimnasio?",
                "answer": "Envía la factura mensual a través del portal de empleados, sección 'Beneficios'. El reembolso (máximo 40€) se incluirá en tu siguiente nómina.",
                "views": 892,
                "helpful": 67
            },
            {
                "id": 4,
                "category": "Desarrollo",
                "question": "¿Cuántas veces al año puedo cambiar de equipo?",
                "answer": "Puedes solicitar rotación una vez al año, sujeto a disponibilidad y aprobación de ambos managers. El proceso toma típicamente 2-3 meses.",
                "views": 445,
                "helpful": 23
            },
            {
                "id": 5,
                "category": "Técnico",
                "question": "¿Cómo accedo al VPN corporativo?",
                "answer": "Solicita acceso en el portal IT. Recibirás las credenciales en 24h. Usa OpenVPN Connect con el archivo de configuración proporcionado.",
                "views": 3421,
                "helpful": 234
            },
            {
                "id": 6,
                "category": "Compensación",
                "question": "¿Cuándo se pagan los bonus?",
                "answer": "Los bonus anuales se pagan en marzo, tras el cierre del año fiscal. Los bonus trimestrales se pagan el mes siguiente al cierre del trimestre.",
                "views": 5623,
                "helpful": 412
            },
            {
                "id": 7,
                "category": "Oficina",
                "question": "¿Hay parking disponible en la oficina?",
                "answer": "Sí, tenemos 50 plazas de parking gratuitas (first come, first served) y convenio con parking cercano (50% descuento).",
                "views": 1234,
                "helpful": 78
            },
            {
                "id": 8,
                "category": "Formación",
                "question": "¿Puedo usar el presupuesto de formación para certificaciones?",
                "answer": "Sí, las certificaciones profesionales están cubiertas. Necesitas aprobación previa de tu manager y compromiso de permanencia de 1 año tras obtenerla.",
                "views": 2156,
                "helpful": 189
            }
        ],
        "metadata": {
            "last_updated": "2025-01-01",
            "total_faqs": 8,
            "categories": ["Vacaciones", "Trabajo Remoto", "Beneficios", "Desarrollo", "Técnico", "Compensación", "Oficina", "Formación"]
        }
    }
    
    with open(data_dir / "faqs.json", 'w', encoding='utf-8') as f:
        json.dump(faqs, f, indent=2, ensure_ascii=False)
    print(f"✅ Creado: {data_dir / 'faqs.json'}")
    
    # 4. Support Tickets CSV
    tickets = [
        ["ticket_id", "date", "user", "category", "subject", "description", "priority", "status", "resolution"],
        ["T001", "2025-01-15", "juan.perez", "VPN", "No puedo conectar al VPN", "El cliente VPN da error de autenticación", "High", "Resolved", "Credenciales reseteadas"],
        ["T002", "2025-01-16", "maria.garcia", "Hardware", "Necesito nuevo laptop", "Mi laptop actual es muy lento para desarrollo", "Medium", "Approved", "Nuevo MacBook Pro aprobado"],
        ["T003", "2025-01-17", "carlos.lopez", "Software", "Licencia de IntelliJ", "Necesito licencia de IntelliJ IDEA Ultimate", "Low", "Resolved", "Licencia asignada"],
        ["T004", "2025-01-18", "ana.martinez", "Acceso", "Acceso a repo privado", "Necesito acceso al repositorio del proyecto X", "High", "Resolved", "Permisos otorgados"],
        ["T005", "2025-01-19", "pedro.sanchez", "Email", "Lista de distribución", "Crear lista all-developers@techcorp.com", "Low", "Pending", "En proceso"],
        ["T006", "2025-01-20", "laura.rodriguez", "VPN", "VPN lento", "La conexión VPN es muy lenta desde casa", "Medium", "Investigating", "Revisando configuración"],
        ["T007", "2025-01-21", "diego.fernandez", "Hardware", "Monitor adicional", "Solicito segundo monitor para home office", "Low", "Approved", "Enviado a domicilio"],
        ["T008", "2025-01-22", "sofia.gonzalez", "Software", "Error en CI/CD", "Pipeline falla en stage de deployment", "Critical", "Resolved", "Fix aplicado al pipeline"],
        ["T009", "2025-01-23", "miguel.torres", "Beneficios", "Reembolso gimnasio", "No recibí reembolso de diciembre", "Medium", "Resolved", "Procesado en siguiente nómina"],
        ["T010", "2025-01-24", "isabel.ramirez", "Formación", "Curso de AWS", "Aprobación para curso AWS Solutions Architect", "Medium", "Approved", "Curso aprobado, inscripción abierta"]
    ]
    
    with open(data_dir / "support_tickets.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(tickets)
    print(f"✅ Creado: {data_dir / 'support_tickets.csv'}")
    
    print("\n✅ Todos los archivos de datos creados exitosamente!")
    
def validate_environment():
    """Validar que el ambiente está correctamente configurado"""
    checks = {
        "Python Version": sys.version.split()[0] >= "3.11",
        "OpenAI API Key": bool(os.getenv("OPENAI_API_KEY")),
        "Data Directory": Path("data").exists(),
        "Source Directory": Path("src").exists(),
        "Notebooks Directory": Path("notebooks").exists()
    }
    
    print("🔍 Validación del Ambiente\n" + "="*40)
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    return all(checks.values())

if __name__ == "__main__":
    import sys
    
    parser = argparse.ArgumentParser(description="Utilidades RAG Workshop")
    parser.add_argument("--create-sample-data", action="store_true",
                      help="Crear datos de ejemplo")
    parser.add_argument("--validate", action="store_true",
                      help="Validar ambiente")
    
    args = parser.parse_args()
    
    if args.create_sample_data:
        create_sample_data()
    elif args.validate:
        if validate_environment():
            print("\n✅ Ambiente listo para el workshop!")
        else:
            print("\n⚠️ Hay problemas con el ambiente. Por favor revisa.")
            sys.exit(1)
    else:
        parser.print_help()