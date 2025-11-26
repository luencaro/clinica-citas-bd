"""
Tests para Validadores
Verifica que todas las validaciones funcionen correctamente
"""
import pytest
from datetime import date, time, timedelta
from validators import UsuarioValidator, PacienteValidator, MedicoValidator, HorarioValidator, CitaValidator
from exceptions import (
    EmailInvalidoError,
    TelefonoInvalidoError,
    ContraseñaDebildError,
    ValidationError
)


class TestUsuarioValidator:
    """Tests para validación de usuarios"""
    
    def test_email_valido(self):
        """Email válido no debe lanzar excepción"""
        UsuarioValidator.validar_email("test@example.com")
        UsuarioValidator.validar_email("user.name+tag@example.co.uk")
    
    def test_email_invalido(self):
        """Email inválido debe lanzar excepción"""
        with pytest.raises(EmailInvalidoError):
            UsuarioValidator.validar_email("invalid-email")
        
        with pytest.raises(EmailInvalidoError):
            UsuarioValidator.validar_email("@example.com")
        
        with pytest.raises(EmailInvalidoError):
            UsuarioValidator.validar_email("test@")
    
    def test_telefono_valido(self):
        """Teléfono válido no debe lanzar excepción"""
        UsuarioValidator.validar_telefono("1234567890")
        UsuarioValidator.validar_telefono("+12345678901")
    
    def test_telefono_invalido(self):
        """Teléfono inválido debe lanzar excepción"""
        with pytest.raises(TelefonoInvalidoError):
            UsuarioValidator.validar_telefono("123")  # Muy corto
        
        with pytest.raises(TelefonoInvalidoError):
            UsuarioValidator.validar_telefono("abc1234567")  # Letras
    
    def test_contraseña_valida(self):
        """Contraseña válida no debe lanzar excepción"""
        UsuarioValidator.validar_contraseña("Password123")
        UsuarioValidator.validar_contraseña("MyP@ssw0rd")
    
    def test_contraseña_invalida(self):
        """Contraseña inválida debe lanzar excepción"""
        # Muy corta
        with pytest.raises(ContraseñaDebildError):
            UsuarioValidator.validar_contraseña("Pass1")
        
        # Sin mayúscula
        with pytest.raises(ContraseñaDebildError):
            UsuarioValidator.validar_contraseña("password123")
        
        # Sin minúscula
        with pytest.raises(ContraseñaDebildError):
            UsuarioValidator.validar_contraseña("PASSWORD123")
        
        # Sin número
        with pytest.raises(ContraseñaDebildError):
            UsuarioValidator.validar_contraseña("Password")
    
    def test_rol_valido(self):
        """Rol válido no debe lanzar excepción"""
        UsuarioValidator.validar_rol("ADMIN")
        UsuarioValidator.validar_rol("MEDICO")
        UsuarioValidator.validar_rol("PACIENTE")
    
    def test_rol_invalido(self):
        """Rol inválido debe lanzar excepción"""
        with pytest.raises(ValidationError):
            UsuarioValidator.validar_rol("SUPERUSER")
        
        with pytest.raises(ValidationError):
            UsuarioValidator.validar_rol("admin")  # Minúsculas


class TestPacienteValidator:
    """Tests para validación de pacientes"""
    
    def test_fecha_nacimiento_valida(self):
        """Fecha de nacimiento válida"""
        fecha_valida = date(1990, 1, 1)
        PacienteValidator.validar_fecha_nacimiento(fecha_valida)
    
    def test_fecha_nacimiento_futura(self):
        """Fecha futura debe lanzar excepción"""
        fecha_futura = date.today() + timedelta(days=1)
        with pytest.raises(ValidationError):
            PacienteValidator.validar_fecha_nacimiento(fecha_futura)
    
    def test_fecha_nacimiento_muy_antigua(self):
        """Fecha muy antigua debe lanzar excepción"""
        fecha_antigua = date(1900, 1, 1)
        with pytest.raises(ValidationError):
            PacienteValidator.validar_fecha_nacimiento(fecha_antigua)
    
    def test_genero_valido(self):
        """Género válido"""
        PacienteValidator.validar_genero("M")
        PacienteValidator.validar_genero("F")
        PacienteValidator.validar_genero(None)  # Opcional
    
    def test_genero_invalido(self):
        """Género inválido debe lanzar excepción"""
        with pytest.raises(ValidationError):
            PacienteValidator.validar_genero("X")


class TestMedicoValidator:
    """Tests para validación de médicos"""
    
    def test_registro_profesional_valido(self):
        """Registro profesional válido"""
        MedicoValidator.validar_registro_profesional("MED-12345")
        MedicoValidator.validar_registro_profesional("REG-ABC-123")
    
    def test_registro_profesional_invalido(self):
        """Registro profesional inválido"""
        with pytest.raises(ValidationError):
            MedicoValidator.validar_registro_profesional("")
        
        with pytest.raises(ValidationError):
            MedicoValidator.validar_registro_profesional("AB")  # Muy corto


class TestHorarioValidator:
    """Tests para validación de horarios"""
    
    def test_horario_valido(self):
        """Horario válido"""
        HorarioValidator.validar_horario(
            dia_semana=1,
            hora_inicio=time(9, 0),
            hora_fin=time(17, 0)
        )
    
    def test_dia_semana_invalido(self):
        """Día de semana inválido"""
        with pytest.raises(ValidationError):
            HorarioValidator.validar_horario(
                dia_semana=8,  # Solo 1-7
                hora_inicio=time(9, 0),
                hora_fin=time(17, 0)
            )
    
    def test_horario_fuera_de_rango(self):
        """Horario fuera del rango permitido (06:00-22:00)"""
        with pytest.raises(ValidationError):
            HorarioValidator.validar_horario(
                dia_semana=1,
                hora_inicio=time(5, 0),  # Antes de 06:00
                hora_fin=time(17, 0)
            )
        
        with pytest.raises(ValidationError):
            HorarioValidator.validar_horario(
                dia_semana=1,
                hora_inicio=time(9, 0),
                hora_fin=time(23, 0)  # Después de 22:00
            )
    
    def test_hora_fin_antes_de_inicio(self):
        """Hora fin debe ser mayor que hora inicio"""
        with pytest.raises(ValidationError):
            HorarioValidator.validar_horario(
                dia_semana=1,
                hora_inicio=time(17, 0),
                hora_fin=time(9, 0)  # Fin antes de inicio
            )


class TestCitaValidator:
    """Tests para validación de citas"""
    
    def test_fecha_cita_valida(self):
        """Fecha de cita futura válida"""
        fecha_futura = date.today() + timedelta(days=7)
        CitaValidator.validar_fecha_cita(fecha_futura)
    
    def test_fecha_cita_pasada(self):
        """Fecha pasada debe lanzar excepción"""
        fecha_pasada = date.today() - timedelta(days=1)
        with pytest.raises(ValidationError):
            CitaValidator.validar_fecha_cita(fecha_pasada)
    
    def test_fecha_cita_muy_futura(self):
        """Fecha muy futura (>6 meses) debe lanzar excepción"""
        fecha_muy_futura = date.today() + timedelta(days=200)
        with pytest.raises(ValidationError):
            CitaValidator.validar_fecha_cita(fecha_muy_futura)
    
    def test_hora_cita_valida(self):
        """Hora en punto exacto o media"""
        CitaValidator.validar_hora_cita(time(10, 0))  # En punto
        CitaValidator.validar_hora_cita(time(10, 30))  # Media
    
    def test_hora_cita_invalida(self):
        """Hora no en punto ni media debe lanzar excepción"""
        with pytest.raises(ValidationError):
            CitaValidator.validar_hora_cita(time(10, 15))  # Cuarto
        
        with pytest.raises(ValidationError):
            CitaValidator.validar_hora_cita(time(10, 45))  # Tres cuartos
    
    def test_motivo_valido(self):
        """Motivo con longitud válida"""
        CitaValidator.validar_motivo("Consulta general")
        CitaValidator.validar_motivo("Dolor de cabeza persistente")
    
    def test_motivo_invalido(self):
        """Motivo muy corto debe lanzar excepción"""
        with pytest.raises(ValidationError):
            CitaValidator.validar_motivo("AB")  # Muy corto
        
        with pytest.raises(ValidationError):
            CitaValidator.validar_motivo("")  # Vacío
    
    def test_estado_valido(self):
        """Estados válidos de cita"""
        CitaValidator.validar_estado("AGENDADA")
        CitaValidator.validar_estado("CANCELADA")
        CitaValidator.validar_estado("REPROGRAMADA")
        CitaValidator.validar_estado("ATENDIDA")
        CitaValidator.validar_estado("NO_ASISTIO")
    
    def test_estado_invalido(self):
        """Estado inválido debe lanzar excepción"""
        with pytest.raises(ValidationError):
            CitaValidator.validar_estado("PENDIENTE")
        
        with pytest.raises(ValidationError):
            CitaValidator.validar_estado("CONFIRMADA")


# Tests adicionales para validaciones combinadas
class TestValidacionesCombinadas:
    """Tests para validaciones que requieren múltiples campos"""
    
    def test_creacion_usuario_completa(self):
        """Validar creación de usuario con todos los campos"""
        UsuarioValidator.validar_creacion_usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com",
            telefono="1234567890",
            contraseña="Password123",
            rol="PACIENTE"
        )
    
    def test_creacion_usuario_datos_invalidos(self):
        """Validar que falla con datos inválidos"""
        with pytest.raises((EmailInvalidoError, ContraseñaDebildError)):
            UsuarioValidator.validar_creacion_usuario(
                nombre="Juan",
                apellido="Pérez",
                email="invalid-email",
                telefono="1234567890",
                contraseña="weak",
                rol="PACIENTE"
            )
    
    def test_creacion_paciente_completa(self):
        """Validar creación de paciente con todos los campos"""
        PacienteValidator.validar_creacion_paciente(
            fecha_nacimiento=date(1990, 1, 1),
            direccion="Calle Test 123",
            genero="M",
            observaciones_medicas=None
        )
    
    def test_creacion_medico_completa(self):
        """Validar creación de médico con todos los campos"""
        MedicoValidator.validar_creacion_medico(
            id_especialidad=1,
            registro_profesional="MED-12345",
            descripcion="Médico general"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
