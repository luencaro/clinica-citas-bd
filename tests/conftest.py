"""
Configuración de tests para pytest
"""
import sys
import os
from pathlib import Path

# Agregar el directorio app al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'app'))

import pytest
from datetime import date, time

# Fixtures compartidos
@pytest.fixture
def sample_usuario_data():
    """Datos de prueba para usuario"""
    return {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'email': 'juan.perez@test.com',
        'telefono': '555-1234',
        'contraseña': 'Password123',
        'rol': 'PACIENTE',
        'activo': True
    }

@pytest.fixture
def sample_paciente_data():
    """Datos de prueba para paciente"""
    return {
        'fecha_nacimiento': date(1990, 5, 15),
        'direccion': 'Calle Test 123',
        'genero': 'M'
    }

@pytest.fixture
def sample_medico_data():
    """Datos de prueba para médico"""
    return {
        'id_especialidad': 1,
        'registro_profesional': 'MED-TEST-123',
        'descripcion': 'Médico de prueba',
        'activo': True
    }

@pytest.fixture
def sample_cita_data():
    """Datos de prueba para cita"""
    return {
        'id_paciente': 1,
        'id_medico': 1,
        'fecha': date(2025, 12, 15),
        'hora': time(10, 0),
        'motivo': 'Consulta general',
        'observaciones': 'Primera consulta'
    }

@pytest.fixture
def sample_horario_data():
    """Datos de prueba para horario"""
    return {
        'id_medico': 1,
        'dia_semana': 1,  # Lunes
        'hora_inicio': time(9, 0),
        'hora_fin': time(17, 0)
    }
