#!/usr/bin/env python3
"""
Sistema de Gestión de Citas Médicas - Django Web Application
Curso: Base de Datos 2025-30-2497
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

def main():
    """Main application entry point"""
    print("\n" + "="*70)
    print("Sistema de Gestión de Citas Médicas - Web Application")
    print("="*70)
    
    # Initialize database connection
    from database.connection import db
    
    print("\n🔌 Conectando a la base de datos...")
    if not db.connect_with_retry():
        print("❌ Error: No se pudo conectar a la base de datos")
        print("   Verifica que el contenedor Docker esté corriendo:")
        print("   docker compose up -d")
        sys.exit(1)
    
    print("✅ Conexión exitosa!")
    
    # Test connection
    success, message = db.test_connection()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        sys.exit(1)
    
    # Import Django
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado?"
        ) from exc
    
    # Run migrations
    print("\n🔄 Verificando migraciones de Django...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Migraciones aplicadas")
    except Exception as e:
        print(f"⚠️  Advertencia: {e}")
    
    # Get server configuration
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = os.getenv('APP_PORT', '5000')
    
    print("\n" + "="*70)
    print(f"🚀 Iniciando servidor web en http://{host}:{port}")
    print("="*70)
    print("\n📋 Accesos del sistema:")
    print("   - URL: http://localhost:5000")
    print("   - Admin: admin@clinica.com / Clinica2025!")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    
    # Start Django development server
    try:
        execute_from_command_line([
            'manage.py',
            'runserver',
            f'{host}:{port}',
            '--noreload'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Cerrando servidor...")
        db.close()
        print("✅ Servidor cerrado correctamente\n")


if __name__ == "__main__":
    main()
