#!/usr/bin/env python3
"""
Script de verificación completo para Workshop RAG 2025
Verifica que todo esté configurado correctamente antes de empezar

Uso:
    python scripts/verify_setup.py
    python scripts/verify_setup.py --quick  # Solo checks básicos
    python scripts/verify_setup.py --fix    # Intenta arreglar problemas
"""

import sys
import os
from pathlib import Path
import subprocess
import time
from typing import Dict, List, Tuple

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

# ===== VERIFICACIONES =====

def check_python_version() -> Tuple[bool, str]:
    """Verifica versión de Python"""
    try:
        version = sys.version.split()[0]
        major, minor = map(int, version.split('.')[:2])

        if major == 3 and minor >= 11:
            return True, f"Python {version}"
        else:
            return False, f"Python {version} (se requiere 3.11+)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_packages() -> List[Tuple[str, bool, str]]:
    """Verifica paquetes instalados"""
    packages = [
        ('openai', '1.45.0'),
        ('langchain', '0.2.11'),
        ('llama_index', '0.10.55'),
        ('chromadb', '0.5.0'),
        ('fastapi', '0.110.0'),
        ('streamlit', '1.35.0'),
        ('pandas', '2.2.0'),
        ('PyPDF2', '3.0.1'),
    ]

    results = []
    for package, expected_version in packages:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')

            # Simplificar nombre para display
            display_name = package.replace('_', '-')
            results.append((display_name, True, version))
        except ImportError:
            results.append((package, False, "No instalado"))

    return results

def check_api_key() -> Tuple[bool, str]:
    """Verifica API key de OpenAI"""
    try:
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            return False, "API Key no configurada en .env"

        if api_key == "sk-YOUR-API-KEY-HERE":
            return False, "API Key es el placeholder por defecto"

        if not api_key.startswith("sk-"):
            return False, "API Key no tiene formato válido (debe empezar con 'sk-')"

        if len(api_key) < 20:
            return False, "API Key parece demasiado corta"

        return True, f"Configurada: {api_key[:7]}..."

    except Exception as e:
        return False, f"Error: {str(e)}"

def check_openai_connection() -> Tuple[bool, str]:
    """Verifica conexión con OpenAI API"""
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return False, "API Key no configurada"

        client = OpenAI(api_key=api_key)

        # Test simple
        start = time.time()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=5
        )
        latency = int((time.time() - start) * 1000)

        return True, f"Conexión exitosa (latencia: {latency}ms)"

    except Exception as e:
        error_msg = str(e).lower()

        if "authentication" in error_msg or "invalid" in error_msg:
            return False, "API Key inválida"
        elif "quota" in error_msg or "insufficient" in error_msg:
            return False, "Sin créditos suficientes en cuenta OpenAI"
        elif "rate" in error_msg:
            return False, "Límite de rate excedido (intenta en 1 minuto)"
        else:
            return False, f"Error de conexión: {str(e)[:100]}"

def check_data_files() -> List[Tuple[str, bool, str]]:
    """Verifica archivos de datos"""
    data_dir = Path("data")
    required_files = [
        "company_handbook.pdf",
        "technical_docs.pdf",
        "faqs.json",
        "support_tickets.csv"
    ]

    results = []
    for filename in required_files:
        filepath = data_dir / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            results.append((filename, True, f"{size_kb:.1f} KB"))
        else:
            results.append((filename, False, "No encontrado"))

    return results

def check_jupyter() -> Tuple[bool, str]:
    """Verifica Jupyter"""
    try:
        import jupyter
        import jupyterlab
        import ipykernel

        return True, "Jupyter Lab instalado"
    except ImportError as e:
        return False, f"Jupyter no instalado completamente"

def check_notebooks() -> List[Tuple[str, bool, str]]:
    """Verifica notebooks del workshop"""
    notebooks_dir = Path("notebooks")
    required_notebooks = [
        "00_inicio.ipynb",
        "01_fundamentos.ipynb",
        "02_arquitectura.ipynb",
        "03_frameworks.ipynb",
        "04_produccion.ipynb",
        "05_proyecto_final.ipynb"
    ]

    results = []
    for notebook in required_notebooks:
        filepath = notebooks_dir / notebook
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            results.append((notebook, True, f"{size_kb:.1f} KB"))
        else:
            results.append((notebook, False, "No encontrado"))

    return results

def check_env_file() -> Tuple[bool, str]:
    """Verifica archivo .env"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if not env_path.exists():
        if env_example_path.exists():
            return False, "Archivo .env no existe (copia .env.example)"
        else:
            return False, "Ni .env ni .env.example existen"

    return True, "Archivo .env existe"

def check_src_modules() -> Tuple[bool, str]:
    """Verifica módulos de src/"""
    src_dir = Path("src")
    required_modules = [
        "shared_config.py",
        "module_1_basics.py",
        "module_2_optimized.py"
    ]

    missing = []
    for module in required_modules:
        if not (src_dir / module).exists():
            missing.append(module)

    if missing:
        return False, f"Faltan módulos: {', '.join(missing)}"

    return True, f"Todos los módulos encontrados ({len(required_modules)})"

# ===== FUNCIÓN PRINCIPAL =====

def main():
    """Ejecuta todas las verificaciones"""

    print_header("🔍 VERIFICACIÓN DE SETUP - RAG WORKSHOP 2025")

    # Cambiar a directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print_info(f"Directorio de trabajo: {project_root}")

    all_checks_passed = True

    # === CHECK 1: Python ===
    print_header("1️⃣ Python Version")
    success, msg = check_python_version()
    if success:
        print_success(msg)
    else:
        print_error(msg)
        all_checks_passed = False

    # === CHECK 2: Paquetes ===
    print_header("2️⃣ Paquetes Instalados")
    packages_results = check_packages()
    installed = sum(1 for _, success, _ in packages_results if success)
    total = len(packages_results)

    for package, success, version in packages_results:
        if success:
            print_success(f"{package:20s} {version}")
        else:
            print_error(f"{package:20s} {version}")
            all_checks_passed = False

    print(f"\n📊 Instalados: {installed}/{total}")

    # === CHECK 3: Jupyter ===
    print_header("3️⃣ Jupyter")
    success, msg = check_jupyter()
    if success:
        print_success(msg)
    else:
        print_error(msg)
        all_checks_passed = False

    # === CHECK 4: Archivo .env ===
    print_header("4️⃣ Configuración (.env)")
    success, msg = check_env_file()
    if success:
        print_success(msg)
    else:
        print_error(msg)
        print_info("Corre: cp .env.example .env")
        all_checks_passed = False

    # === CHECK 5: API Key ===
    print_header("5️⃣ OpenAI API Key")
    success, msg = check_api_key()
    if success:
        print_success(msg)
    else:
        print_error(msg)
        print_info("Configura tu API key en el archivo .env")
        print_info("Obtén una en: https://platform.openai.com/api-keys")
        all_checks_passed = False

    # === CHECK 6: Conexión OpenAI ===
    if success:  # Solo si la API key está configurada
        print_header("6️⃣ Conexión con OpenAI")
        print_info("Probando conexión (esto puede tomar unos segundos)...")
        success, msg = check_openai_connection()
        if success:
            print_success(msg)
        else:
            print_error(msg)
            all_checks_passed = False
    else:
        print_header("6️⃣ Conexión con OpenAI")
        print_warning("Saltado (API key no configurada)")

    # === CHECK 7: Archivos de datos ===
    print_header("7️⃣ Archivos de Datos")
    data_results = check_data_files()
    found = sum(1 for _, success, _ in data_results if success)
    total = len(data_results)

    for filename, success, info in data_results:
        if success:
            print_success(f"{filename:25s} {info}")
        else:
            print_error(f"{filename:25s} {info}")
            all_checks_passed = False

    print(f"\n📊 Encontrados: {found}/{total}")

    if found < total:
        print_info("Genera archivos faltantes con: python src/utils.py --create-sample-data")

    # === CHECK 8: Notebooks ===
    print_header("8️⃣ Notebooks del Workshop")
    notebooks_results = check_notebooks()
    found = sum(1 for _, success, _ in notebooks_results if success)
    total = len(notebooks_results)

    for notebook, success, info in notebooks_results:
        if success:
            print_success(f"{notebook:30s} {info}")
        else:
            print_error(f"{notebook:30s} {info}")
            all_checks_passed = False

    print(f"\n📊 Encontrados: {found}/{total}")

    # === CHECK 9: Módulos src/ ===
    print_header("9️⃣ Módulos de Código")
    success, msg = check_src_modules()
    if success:
        print_success(msg)
    else:
        print_error(msg)
        all_checks_passed = False

    # === RESUMEN FINAL ===
    print_header("📊 RESUMEN DE VERIFICACIÓN")

    if all_checks_passed:
        print_success("¡TODO VERIFICADO CORRECTAMENTE! 🎉")
        print()
        print(f"{Colors.GREEN}✨ Estás listo para empezar el workshop{Colors.END}")
        print()
        print(f"{Colors.BOLD}Siguiente paso:{Colors.END}")
        print("  1. Abre Jupyter Lab: jupyter lab")
        print("  2. Navega a: notebooks/00_inicio.ipynb")
        print("  3. Ejecuta las celdas del notebook")
        print()
        return 0
    else:
        print_error("ALGUNAS VERIFICACIONES FALLARON")
        print()
        print(f"{Colors.YELLOW}Soluciones comunes:{Colors.END}")
        print("  1. API Key: Edita .env y añade tu OPENAI_API_KEY")
        print("  2. Paquetes: pip install -r requirements.txt")
        print("  3. Datos: python src/utils.py --create-sample-data")
        print()
        print(f"{Colors.YELLOW}Si necesitas ayuda:{Colors.END}")
        print("  - Revisa: README.md")
        print("  - Contacta: aromero@secture.com")
        print()
        return 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Verificar setup del workshop')
    parser.add_argument('--quick', action='store_true', help='Solo checks básicos')
    parser.add_argument('--fix', action='store_true', help='Intentar arreglar problemas')

    args = parser.parse_args()

    exit_code = main()
    sys.exit(exit_code)
