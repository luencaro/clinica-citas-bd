#!/usr/bin/env python3
"""
Test de autenticación
"""

import sys
import os
sys.path.insert(0, '/app')

from dotenv import load_dotenv
load_dotenv()

from database.connection import db
from services.usuario_service import UsuarioService

# Conectar a la base de datos
if not db.connect_with_retry():
    print("❌ No se pudo conectar a la base de datos")
    sys.exit(1)

# Test de autenticación
usuario_service = UsuarioService()

print("=" * 70)
print("TEST DE AUTENTICACIÓN")
print("=" * 70)

# Test 1: Admin
print("\n1. Probando admin@clinica.com con Clinica2025!")
try:
    user = usuario_service.autenticar('admin@clinica.com', 'Clinica2025!')
    print(f"✅ Login exitoso: {user.nombre} {user.apellido} ({user.rol})")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Paciente que no existe
print("\n2. Probando carlos.garcia@email.com con Paciente2025!")
try:
    user = usuario_service.autenticar('carlos.garcia@email.com', 'Paciente2025!')
    print(f"✅ Login exitoso: {user.nombre} {user.apellido} ({user.rol})")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Verificar usuario existente
print("\n3. Probando luis.gomez@email.com con Clinica2025!")
try:
    user = usuario_service.autenticar('luis.gomez@email.com', 'Clinica2025!')
    print(f"✅ Login exitoso: {user.nombre} {user.apellido} ({user.rol})")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Médico
print("\n4. Probando maria.lopez@clinica.com con Clinica2025!")
try:
    user = usuario_service.autenticar('maria.lopez@clinica.com', 'Clinica2025!')
    print(f"✅ Login exitoso: {user.nombre} {user.apellido} ({user.rol})")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("Usuarios disponibles en la base de datos:")
print("=" * 70)
from repositories.usuario_repository import UsuarioRepository
repo = UsuarioRepository()
usuarios = repo.find_all()
for u in usuarios[:10]:
    print(f"- {u.email} ({u.rol})")
