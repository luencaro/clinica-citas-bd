#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del proyecto
"""

import sys
import os
from pathlib import Path
from datetime import date, time, timedelta

# Agregar app al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'app'))

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if details and not passed:
        print(f"       {Colors.YELLOW}{details}{Colors.END}")

def run_validator_tests():
    """Tests de validadores"""
    print_header("TESTS DE VALIDADORES")
    
    from validators import UsuarioValidator, CitaValidator, HorarioValidator
    from exceptions import FormatoInvalidoError, CampoRequeridoError
    
    passed = 0
    failed = 0
    
    # Test 1: Email válido
    try:
        UsuarioValidator.validar_email("test@example.com")
        print_test("Email válido", True)
        passed += 1
    except Exception as e:
        print_test("Email válido", False, str(e))
        failed += 1
    
    # Test 2: Email inválido
    try:
        UsuarioValidator.validar_email("invalid-email")
        print_test("Email inválido debe fallar", False, "No lanzó excepción")
        failed += 1
    except FormatoInvalidoError:
        print_test("Email inválido debe fallar", True)
        passed += 1
    except Exception as e:
        print_test("Email inválido debe fallar", False, str(e))
        failed += 1
    
    # Test 3: Contraseña válida
    try:
        UsuarioValidator.validar_contraseña("Password123")
        print_test("Contraseña válida", True)
        passed += 1
    except Exception as e:
        print_test("Contraseña válida", False, str(e))
        failed += 1
    
    # Test 4: Contraseña débil
    try:
        UsuarioValidator.validar_contraseña("weak")
        print_test("Contraseña débil debe fallar", False, "No lanzó excepción")
        failed += 1
    except FormatoInvalidoError:
        print_test("Contraseña débil debe fallar", True)
        passed += 1
    except Exception as e:
        print_test("Contraseña débil debe fallar", False, str(e))
        failed += 1
    
    # Test 5: Teléfono válido
    try:
        UsuarioValidator.validar_telefono("1234567890")
        print_test("Teléfono válido", True)
        passed += 1
    except Exception as e:
        print_test("Teléfono válido", False, str(e))
        failed += 1
    
    # Test 6: Fecha cita futura
    try:
        fecha_futura = date.today() + timedelta(days=7)
        CitaValidator.validar_fecha_cita(fecha_futura)
        print_test("Fecha futura válida", True)
        passed += 1
    except Exception as e:
        print_test("Fecha futura válida", False, str(e))
        failed += 1
    
    # Test 7: Fecha pasada debe fallar
    try:
        fecha_pasada = date.today() - timedelta(days=1)
        CitaValidator.validar_fecha_cita(fecha_pasada)
        print_test("Fecha pasada debe fallar", False, "No lanzó excepción")
        failed += 1
    except Exception:
        print_test("Fecha pasada debe fallar", True)
        passed += 1
    
    # Test 8: Hora válida (en punto)
    try:
        CitaValidator.validar_hora_cita(time(10, 0))
        print_test("Hora en punto válida", True)
        passed += 1
    except Exception as e:
        print_test("Hora en punto válida", False, str(e))
        failed += 1
    
    # Test 9: Hora válida (media)
    try:
        CitaValidator.validar_hora_cita(time(10, 30))
        print_test("Hora media válida", True)
        passed += 1
    except Exception as e:
        print_test("Hora media válida", False, str(e))
        failed += 1
    
    # Test 10: Hora inválida (cuarto)
    try:
        CitaValidator.validar_hora_cita(time(10, 15))
        print_test("Hora cuarto debe fallar", False, "No lanzó excepción")
        failed += 1
    except Exception:
        print_test("Hora cuarto debe fallar", True)
        passed += 1
    
    # Test 11: Horario laboral válido
    try:
        HorarioValidator.validar_rango_horario(time(9, 0), time(17, 0))
        print_test("Horario laboral válido", True)
        passed += 1
    except Exception as e:
        print_test("Horario laboral válido", False, str(e))
        failed += 1
    
    # Test 12: Horario fuera de rango (hora fin antes de inicio)
    try:
        HorarioValidator.validar_rango_horario(time(17, 0), time(9, 0))
        print_test("Horario invertido debe fallar", False, "No lanzó excepción")
        failed += 1
    except Exception:
        print_test("Horario invertido debe fallar", True)
        passed += 1
    
    return passed, failed


def run_model_tests():
    """Tests de modelos"""
    print_header("TESTS DE MODELOS")
    
    from models.usuario import Usuario
    from models.paciente import Paciente
    from models.cita import Cita
    from models.horario_medico import HorarioMedico
    
    passed = 0
    failed = 0
    
    # Test 1: Usuario roles
    try:
        usuario = Usuario(
            id_usuario=1,
            nombre="Admin",
            apellido="Test",
            email="admin@test.com",
            telefono="1234567890",
            contraseña="hashed",
            rol="ADMIN",
            activo=True,
            fecha_creacion=date.today()
        )
        assert usuario.es_admin() == True
        assert usuario.es_medico() == False
        print_test("Usuario identificación de roles", True)
        passed += 1
    except Exception as e:
        print_test("Usuario identificación de roles", False, str(e))
        failed += 1
    
    # Test 2: Paciente edad
    try:
        paciente = Paciente(
            id_paciente=1,
            id_usuario=1,
            fecha_nacimiento=date(1990, 1, 1),
            direccion="Calle 123"
        )
        edad = paciente.edad
        assert edad >= 30
        print_test("Paciente cálculo de edad", True)
        passed += 1
    except Exception as e:
        print_test("Paciente cálculo de edad", False, str(e))
        failed += 1
    
    # Test 3: Cita estados
    try:
        cita = Cita(
            id_cita=1,
            id_paciente=1,
            id_medico=1,
            fecha=date.today() + timedelta(days=7),
            hora=time(10, 0),
            motivo="Test",
            estado="AGENDADA"
        )
        assert cita.esta_pendiente() == True
        assert cita.puede_cancelarse() == True
        assert cita.puede_reprogramarse() == True
        print_test("Cita transiciones de estado", True)
        passed += 1
    except Exception as e:
        print_test("Cita transiciones de estado", False, str(e))
        failed += 1
    
    # Test 4: Cita cancelada no puede cancelarse
    try:
        cita_cancelada = Cita(
            id_cita=2,
            id_paciente=1,
            id_medico=1,
            fecha=date.today() + timedelta(days=7),
            hora=time(11, 0),
            motivo="Test",
            estado="CANCELADA"
        )
        assert cita_cancelada.puede_cancelarse() == False
        print_test("Cita cancelada no puede cancelarse", True)
        passed += 1
    except Exception as e:
        print_test("Cita cancelada no puede cancelarse", False, str(e))
        failed += 1
    
    # Test 5: Horario validación de hora
    try:
        horario = HorarioMedico(
            id_horario=1,
            id_medico=1,
            dia_semana=1,
            hora_inicio=time(9, 0),
            hora_fin=time(17, 0)
        )
        assert horario.esta_en_horario(time(10, 0)) == True
        assert horario.esta_en_horario(time(8, 0)) == False
        print_test("Horario validación de hora en rango", True)
        passed += 1
    except Exception as e:
        print_test("Horario validación de hora en rango", False, str(e))
        failed += 1
    
    # Test 6: Horario obtener día nombre
    try:
        horario = HorarioMedico(
            id_horario=1,
            id_medico=1,
            dia_semana=1,
            hora_inicio=time(9, 0),
            hora_fin=time(17, 0)
        )
        assert horario.nombre_dia == "Lunes"
        print_test("Horario nombre del día", True)
        passed += 1
    except Exception as e:
        print_test("Horario nombre del día", False, str(e))
        failed += 1
    
    return passed, failed


def run_exception_tests():
    """Tests de excepciones"""
    print_header("TESTS DE EXCEPCIONES")
    
    from exceptions import (
        EmailDuplicadoError,
        CitaNoDisponibleError,
        UsuarioNoEncontradoError,
        FechaPasadaError
    )
    
    passed = 0
    failed = 0
    
    # Test 1: Excepciones pueden instanciarse
    try:
        exc = EmailDuplicadoError("Email duplicado")
        assert "duplicado" in str(exc).lower()
        print_test("Excepción EmailDuplicadoError", True)
        passed += 1
    except Exception as e:
        print_test("Excepción EmailDuplicadoError", False, str(e))
        failed += 1
    
    # Test 2: Excepción Cita
    try:
        exc = CitaNoDisponibleError("Horario no disponible")
        assert "disponible" in str(exc).lower()
        print_test("Excepción CitaNoDisponibleError", True)
        passed += 1
    except Exception as e:
        print_test("Excepción CitaNoDisponibleError", False, str(e))
        failed += 1
    
    # Test 3: Excepción Usuario
    try:
        exc = UsuarioNoEncontradoError("Usuario no encontrado")
        assert "usuario" in str(exc).lower()
        print_test("Excepción UsuarioNoEncontradoError", True)
        passed += 1
    except Exception as e:
        print_test("Excepción UsuarioNoEncontradoError", False, str(e))
        failed += 1
    
    # Test 4: Excepción Fecha
    try:
        exc = FechaPasadaError("Fecha en el pasado")
        assert "fecha" in str(exc).lower()
        print_test("Excepción FechaPasadaError", True)
        passed += 1
    except Exception as e:
        print_test("Excepción FechaPasadaError", False, str(e))
        failed += 1
    
    return passed, failed


def main():
    """Ejecuta todos los tests"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{'SISTEMA DE TESTS - Clínica de Citas Médicas':^60}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    
    total_passed = 0
    total_failed = 0
    
    # Ejecutar tests de validadores
    passed, failed = run_validator_tests()
    total_passed += passed
    total_failed += failed
    
    # Ejecutar tests de modelos
    passed, failed = run_model_tests()
    total_passed += passed
    total_failed += failed
    
    # Ejecutar tests de excepciones
    passed, failed = run_exception_tests()
    total_passed += passed
    total_failed += failed
    
    # Resumen final
    print_header("RESUMEN FINAL")
    
    total_tests = total_passed + total_failed
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"{Colors.BOLD}Total de tests ejecutados: {total_tests}{Colors.END}")
    print(f"{Colors.GREEN}✓ Pasados: {total_passed}{Colors.END}")
    print(f"{Colors.RED}✗ Fallados: {total_failed}{Colors.END}")
    print(f"{Colors.BOLD}Tasa de éxito: {success_rate:.1f}%{Colors.END}\n")
    
    if total_failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ¡TODOS LOS TESTS PASARON!{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Hay tests que requieren atención{Colors.END}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
