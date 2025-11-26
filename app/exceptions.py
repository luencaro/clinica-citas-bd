"""
Excepciones personalizadas del dominio
"""


class DomainException(Exception):
    """Excepción base para errores del dominio"""
    pass


# ============================================================================
# Excepciones de Usuario
# ============================================================================

class UsuarioException(DomainException):
    """Excepción base para errores relacionados con usuarios"""
    pass


class EmailDuplicadoError(UsuarioException):
    """El email ya está registrado en el sistema"""
    pass


class TelefonoDuplicadoError(UsuarioException):
    """El teléfono ya está registrado en el sistema"""
    pass


class UsuarioNoEncontradoError(UsuarioException):
    """El usuario no fue encontrado"""
    pass


class CredencialesInvalidasError(UsuarioException):
    """Credenciales de acceso inválidas"""
    pass


# ============================================================================
# Excepciones de Paciente
# ============================================================================

class PacienteException(DomainException):
    """Excepción base para errores relacionados con pacientes"""
    pass


class EdadInvalidaError(PacienteException):
    """La edad del paciente no es válida"""
    pass


class PacienteNoEncontradoError(PacienteException):
    """El paciente no fue encontrado"""
    pass


# ============================================================================
# Excepciones de Médico
# ============================================================================

class MedicoException(DomainException):
    """Excepción base para errores relacionados con médicos"""
    pass


class MedicoNoEncontradoError(MedicoException):
    """El médico no fue encontrado"""
    pass


class MedicoInactivoError(MedicoException):
    """El médico no está activo"""
    pass


class RegistroProfesionalDuplicadoError(MedicoException):
    """El registro profesional ya existe"""
    pass


# ============================================================================
# Excepciones de Horario
# ============================================================================

class HorarioException(DomainException):
    """Excepción base para errores relacionados con horarios"""
    pass


class HorarioInvalidoError(HorarioException):
    """El horario no es válido"""
    pass


class HorarioSuperposicionError(HorarioException):
    """El horario se superpone con otro existente"""
    pass


class FueraDeHorarioError(HorarioException):
    """La hora solicitada está fuera del horario del médico"""
    pass


# ============================================================================
# Excepciones de Cita
# ============================================================================

class CitaException(DomainException):
    """Excepción base para errores relacionados con citas"""
    pass


class CitaNoEncontradaError(CitaException):
    """La cita no fue encontrada"""
    pass


class CitaNoDisponibleError(CitaException):
    """El horario no está disponible para agendar cita"""
    pass


class CitaDuplicadaError(CitaException):
    """Ya existe una cita en ese horario"""
    pass


class FechaPasadaError(CitaException):
    """No se pueden agendar citas en fechas pasadas"""
    pass


class EstadoCitaInvalidoError(CitaException):
    """El estado de la cita no permite la operación solicitada"""
    pass


class CitaNoPuedeCancelarseError(CitaException):
    """La cita no puede ser cancelada en su estado actual"""
    pass


class CitaNoPuedeReprogramarseError(CitaException):
    """La cita no puede ser reprogramada en su estado actual"""
    pass


# ============================================================================
# Excepciones de Especialidad
# ============================================================================

class EspecialidadException(DomainException):
    """Excepción base para errores relacionados con especialidades"""
    pass


class EspecialidadNoEncontradaError(EspecialidadException):
    """La especialidad no fue encontrada"""
    pass


class EspecialidadDuplicadaError(EspecialidadException):
    """La especialidad ya existe"""
    pass


# ============================================================================
# Excepciones de Validación
# ============================================================================

class ValidationException(DomainException):
    """Excepción base para errores de validación"""
    pass


class CampoRequeridoError(ValidationException):
    """Un campo requerido no fue proporcionado"""
    pass


class FormatoInvalidoError(ValidationException):
    """El formato de un campo no es válido"""
    pass


class ValorFueraDeRangoError(ValidationException):
    """Un valor está fuera del rango permitido"""
    pass
