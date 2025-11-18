#!/usr/bin/env python3
"""
Sistema de Gestión de Citas Médicas
Curso: Base de Datos 2025-30-2497
"""

import sys
import os
import time

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from config import db_config
from database import db

def main():
    """Main application entry point"""
    print("\n" + "="*70)
    print("Sistema de Gestión de Citas Médicas")
    print("="*70)
    
    print("\nConectando a la base de datos...")
    
    if not db.connect_with_retry():
        print("❌ Error: No se pudo conectar a la base de datos")
        sys.exit(1)
    
    print("✅ Conexión exitosa!")
    
    # Test connection
    success, message = db.test_connection()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    # Get table count
    try:
        tables = db.get_all_tables()
        print(f"✅ Tablas en la base de datos: {len(tables)}")
        for table in tables:
            print(f"   - {table}")
    except Exception as e:
        print(f"❌ Error obteniendo tablas: {e}")
    
    print("\n" + "="*70)
    print("Sistema inicializado. Presiona Ctrl+C para salir...")
    print("="*70 + "\n")
    
    # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Cerrando sistema...")
        db.close()
        print("✅ Sistema cerrado correctamente\n")

if __name__ == "__main__":
    main()
