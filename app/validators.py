"""
Validadores de reglas de negocio
"""

import re
from datetime import date, time, datetime
from typing import Optional

from exceptions import (
    CampoRequeridoError,
    FormatoInvalidoError,
    ValorFueraDeRangoError,
    EdadInvalidaError,
    HorarioInvalidoError,
    FechaPasadaError
)


class Validator:
    """Clase base para validadores"""
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida formato de email"""
        if not email:
            raise CampoRequeridoError("El email es requerido")
        
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise FormatoInvalidoError(f"Email inválido: {email}")
        
        return True
    
    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """Valida formato de teléfono"""
        if not telefono:
            raise CampoRequeridoError("El teléfono es requerido")
        
        # Permitir formatos: +57 XXX XXX XXXX, 3XX XXX XXXX, etc.
        telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
        
        if not telefono_limpio.isdigit():
            raise FormatoInvalidoError(f"Teléfono inválido: {telefono}")
        
        if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
            raise FormatoInvalidoError(f"Longitud de teléfono inválida: {telefono}")
        
        return True
    
    @staticmethod
    def validar_contraseña(contraseña: str, min_length: int = 8) -> bool:
        """Valida contraseña"""
        if not contraseña:
            raise CampoRequeridoError("La contraseña es requerida")
        
        if len(contraseña) < min_length:
            raise FormatoInvalidoError(
                f"La contraseña debe tener al menos {min_length} caracteres"
            )
        
        # Al menos una mayúscula, una minúscula y un número
        if not re.search(r'[A-Z]', contraseña):
            raise FormatoInvalidoError("La contraseña debe contener al menos una mayúscula")
        
        if not re.search(r'[a-z]', contraseña):
            raise FormatoInvalidoError("La contraseña debe contener al menos una minúscula")
        
        if not re.search(r'\d', contraseña):
            raise FormatoInvalidoError("La contraseña debe contener al menos un número")
        
        return True
    
    @staticmethod
    def validar_nombre(nombre: str, campo: str = "nombre") -> bool:
        """Valida nombre o apellido"""
        if not nombre:
            raise CampoRequeridoError(f"El {campo} es requerido")
        
        if len(nombre) < 2:
            raise FormatoInvalidoError(f"El {campo} debe tener al menos 2 caracteres")
        
        if len(nombre) > 100:
            raise FormatoInvalidoError(f"El {campo} no puede exceder 100 caracteres")
        
        # Solo letras, espacios y algunos caracteres especiales
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\'-]+$', nombre):
            raise FormatoInvalidoError(f"{campo} contiene caracteres inválidos")
        
        return True


class UsuarioValidator(Validator):
    """Validador para usuarios"""
    
    @staticmethod
    def validar_rol(rol: str) -> bool:
        """Valida rol de usuario"""
        roles_validos = ['ADMIN', 'MEDICO', 'PACIENTE']
        if rol not in roles_validos:
            raise ValorFueraDeRangoError(
                f"Rol inválido: {rol}. Debe ser uno de {roles_validos}"
            )
        return True
    
    @staticmethod
    def validar_creacion_usuario(
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        contraseña: str,
        rol: str
    ) -> bool:
        """Valida datos para crear usuario"""
        Validator.validar_nombre(nombre, "nombre")
        Validator.validar_nombre(apellido, "apellido")
        Validator.validar_email(email)
        Validator.validar_telefono(telefono)
        Validator.validar_contraseña(contraseña)
        UsuarioValidator.validar_rol(rol)
        return True


class PacienteValidator(Validator):
    """Validador para pacientes"""
    
    @staticmethod
    def validar_fecha_nacimiento(fecha_nac: date) -> bool:
        """Valida fecha de nacimiento"""
        if not fecha_nac:
            raise CampoRequeridoError("La fecha de nacimiento es requerida")
        
        hoy = date.today()
        if fecha_nac >= hoy:
            raise FechaPasadaError("La fecha de nacimiento debe ser anterior a hoy")
        
        # Calcular edad
        edad = hoy.year - fecha_nac.year - (
            (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day)
        )
        
        if edad < 0:
            raise EdadInvalidaError("Edad inválida")
        
        if edad > 150:
            raise EdadInvalidaError("Edad no realista")
        
        return True


class MedicoValidator(Validator):
    """Validador para médicos"""
    
    @staticmethod
    def validar_registro_profesional(registro: str) -> bool:
        """Valida registro profesional"""
        if not registro:
            raise CampoRequeridoError("El registro profesional es requerido")
        
        if len(registro) < 5:
            raise FormatoInvalidoError(
                "El registro profesional debe tener al menos 5 caracteres"
            )
        
        if len(registro) > 50:
            raise FormatoInvalidoError(
                "El registro profesional no puede exceder 50 caracteres"
            )
        
        return True


class HorarioValidator(Validator):
    """Validador para horarios"""
    
    @staticmethod
    def validar_dia_semana(dia: int) -> bool:
        """Valida día de la semana"""
        if not 1 <= dia <= 7:
            raise ValorFueraDeRangoError(
                f"Día de semana inválido: {dia}. Debe estar entre 1 y 7"
            )
        return True
    
    @staticmethod
    def validar_rango_horario(hora_inicio: time, hora_fin: time) -> bool:
        """Valida rango de horario"""
        if not hora_inicio:
            raise CampoRequeridoError("La hora de inicio es requerida")
        
        if not hora_fin:
            raise CampoRequeridoError("La hora de fin es requerida")
        
        if hora_inicio >= hora_fin:
            raise HorarioInvalidoError(
                "La hora de inicio debe ser menor que la hora de fin"
            )
        
        # Validar horario laboral razonable (6:00 - 22:00)
        hora_min = time(6, 0)
        hora_max = time(22, 0)
        
        if hora_inicio < hora_min or hora_inicio > hora_max:
            raise HorarioInvalidoError(
                f"La hora de inicio debe estar entre {hora_min} y {hora_max}"
            )
        
        if hora_fin < hora_min or hora_fin > hora_max:
            raise HorarioInvalidoError(
                f"La hora de fin debe estar entre {hora_min} y {hora_max}"
            )
        
        return True


class CitaValidator(Validator):
    """Validador para citas"""
    
    @staticmethod
    def validar_fecha_cita(fecha: date) -> bool:
        """Valida fecha de cita"""
        if not fecha:
            raise CampoRequeridoError("La fecha de la cita es requerida")
        
        hoy = date.today()
        if fecha < hoy:
            raise FechaPasadaError(
                "No se pueden agendar citas en fechas pasadas"
            )
        
        # No permitir citas con más de 6 meses de anticipación
        meses_adelante = (fecha.year - hoy.year) * 12 + (fecha.month - hoy.month)
        if meses_adelante > 6:
            raise ValorFueraDeRangoError(
                "No se pueden agendar citas con más de 6 meses de anticipación"
            )
        
        return True
    
    @staticmethod
    def validar_hora_cita(hora: time) -> bool:
        """Valida hora de cita"""
        if not hora:
            raise CampoRequeridoError("La hora de la cita es requerida")
        
        # Validar que sea hora en punto o media hora
        if hora.minute not in [0, 30]:
            raise FormatoInvalidoError(
                "Las citas solo pueden agendarse en punto o media hora"
            )
        
        return True
    
    @staticmethod
    def validar_motivo(motivo: str) -> bool:
        """Valida motivo de cita"""
        if not motivo:
            raise CampoRequeridoError("El motivo de la cita es requerido")
        
        if len(motivo) < 10:
            raise FormatoInvalidoError(
                "El motivo debe tener al menos 10 caracteres"
            )
        
        if len(motivo) > 500:
            raise FormatoInvalidoError(
                "El motivo no puede exceder 500 caracteres"
            )
        
        return True
    
    @staticmethod
    def validar_estado(estado: str) -> bool:
        """Valida estado de cita"""
        estados_validos = ['AGENDADA', 'CANCELADA', 'REPROGRAMADA', 'ATENDIDA']
        if estado not in estados_validos:
            raise ValorFueraDeRangoError(
                f"Estado inválido: {estado}. Debe ser uno de {estados_validos}"
            )
        return True
