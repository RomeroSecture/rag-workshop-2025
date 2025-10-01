"""
Health Check Script - RAG Workshop 2025
Verifica que todo el ambiente está correctamente configurado
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

def print_header(title):
    """Imprimir header formateado"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"🐍 Python: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 11:
        print("   ✅ Versión correcta (3.11+)")
        return True
    else:
        print("   ⚠️  Se recomienda Python 3.11+")
        return False

def check_dependencies():
    """Verificar dependencias principales"""
    dependencies = {
        "openai": "OpenAI SDK",
        "chromadb": "ChromaDB",
        "langchain": "LangChain",
        "llama_index": "LlamaIndex",
        "fastapi": "FastAPI",
        "streamlit": "Streamlit",
        "pandas": "Pandas",
        "jupyter": "Jupyter",
        "reportlab": "ReportLab"
    }

    all_ok = True
    for module, name in dependencies.items():
        try:
            imported = __import__(module)
            version = getattr(imported, "__version__", "unknown")
            print(f"✅ {name:20s} v{version}")
        except ImportError:
            print(f"❌ {name:20s} NO INSTALADO")
            all_ok = False

    return all_ok

def check_api_key():
    """Verificar API key"""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "")

    if not api_key:
        print("❌ OPENAI_API_KEY no configurada")
        return False

    if not api_key.startswith("sk-"):
        print("⚠️  OPENAI_API_KEY no parece válida (debe empezar con 'sk-')")
        return False

    if len(api_key) < 20:
        print("⚠️  OPENAI_API_KEY parece demasiado corta")
        return False

    print(f"✅ API Key configurada: {api_key[:10]}...{api_key[-4:]}")
    return True

def check_data_files():
    """Verificar archivos de datos"""
    data_dir = Path("data")
    required_files = [
        "company_handbook.pdf",
        "technical_docs.pdf",
        "faqs.json",
        "support_tickets.csv"
    ]

    all_ok = True
    for filename in required_files:
        file_path = data_dir / filename
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"✅ {filename:25s} ({size_kb:.1f} KB)")
        else:
            print(f"❌ {filename:25s} FALTANTE")
            all_ok = False

    return all_ok

def check_directories():
    """Verificar estructura de directorios"""
    required_dirs = [
        "data",
        "data/processed",
        "data/vectordb",
        "data/cache",
        "src",
        "notebooks",
        "tests",
        "docs",
        "logs"
    ]

    all_ok = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"⚠️  {dir_path}/ no existe (se creará si es necesario)")
            if dir_path in ["data", "src", "notebooks"]:
                all_ok = False

    return all_ok

def check_openai_connection():
    """Verificar conexión con OpenAI"""
    try:
        from openai import OpenAI
        load_dotenv()

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Test simple
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=5
        )

        print(f"✅ Conexión exitosa con OpenAI")
        print(f"   Modelo: {response.model}")
        print(f"   Tokens usados: {response.usage.total_tokens}")
        return True

    except Exception as e:
        print(f"❌ Error conectando con OpenAI: {e}")
        return False

def main():
    """Función principal"""
    print("\n🏥 HEALTH CHECK - RAG WORKSHOP 2025")

    results = {}

    # Python
    print_header("Python Version")
    results["python"] = check_python_version()

    # Dependencias
    print_header("Dependencies")
    results["dependencies"] = check_dependencies()

    # API Key
    print_header("API Key")
    results["api_key"] = check_api_key()

    # Directorios
    print_header("Directory Structure")
    results["directories"] = check_directories()

    # Archivos de datos
    print_header("Data Files")
    results["data_files"] = check_data_files()

    # Conexión OpenAI (opcional)
    if results["api_key"]:
        print_header("OpenAI Connection")
        results["openai"] = check_openai_connection()

    # Resumen
    print_header("SUMMARY")
    passed = sum(results.values())
    total = len(results)

    print(f"Verificaciones pasadas: {passed}/{total}")

    if passed == total:
        print("\n🎉 ¡TODO PERFECTO! Listo para el workshop.")
        return 0
    else:
        print("\n⚠️  Hay algunos issues que resolver.")
        print("\n📚 Consulta docs/TROUBLESHOOTING.md para soluciones")
        print("📧 Contacto: aromero@secture.com")
        return 1

if __name__ == "__main__":
    sys.exit(main())
