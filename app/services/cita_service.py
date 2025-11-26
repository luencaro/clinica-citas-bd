"""
Servicio de Cita - Lógica de negocio crítica
"""

from typing import List, Optional
from datetime import date, time, datetime

from models.cita import Cita
from repositories.cita_repository import CitaRepository
from repositories.medico_repository import MedicoRepository
from repositories.paciente_repository import PacienteRepository
from repositories.horario_repository import HorarioRepository
from repositories.notificacion_repository import NotificacionRepository
from validators import CitaValidator
from exceptions import (
    CitaNoEncontradaError,
    CitaNoDisponibleError,
    CitaDuplicadaError,
    FechaPasadaError,
    FueraDeHorarioError,
    EstadoCitaInvalidoError,
    CitaNoPuedeCancelarseError,
    CitaNoPuedeReprogramarseError,
    MedicoNoEncontradoError,
    MedicoInactivoError,
    PacienteNoEncontradoError
)


class CitaService:
    """
    Servicio para gestionar citas
    Implementa TODAS las reglas de negocio críticas del sistema
    """
    
    def __init__(self):
        self.repo = CitaRepository()
        self.medico_repo = MedicoRepository()
        self.paciente_repo = PacienteRepository()
        self.horario_repo = HorarioRepository()
        self.notif_repo = NotificacionRepository()
    
    def agendar_cita(
        self,
        id_paciente: int,
        id_medico: int,
        fecha: date,
        hora: time,
        motivo: str,
        observaciones: str = None
    ) -> Cita:
        """
        Agenda una nueva cita con validaciones completas
        
        Reglas de negocio:
        1. Paciente debe existir
        2. Médico debe existir y estar activo
        3. Fecha debe ser futura
        4. Hora debe estar en horario del médico
        5. No debe existir otra cita en ese horario
        6. Motivo debe ser válido
        """
        # Validar datos básicos
        CitaValidator.validar_fecha_cita(fecha)
        CitaValidator.validar_hora_cita(hora)
        CitaValidator.validar_motivo(motivo)
        
        # Validar paciente
        paciente = self.paciente_repo.find_by_id(id_paciente, 'id_paciente')
        if not paciente:
            raise PacienteNoEncontradoError(f"Paciente {id_paciente} no encontrado")
        
        # Validar médico
        medico = self.medico_repo.find_by_id(id_medico, 'id_medico')
        if not medico:
            raise MedicoNoEncontradoError(f"Médico {id_medico} no encontrado")
        
        if not medico.activo:
            raise MedicoInactivoError(f"El médico {id_medico} no está activo")
        
        # Validar disponibilidad del médico
        self._validar_disponibilidad_medico(id_medico, fecha, hora)
        
        # Verificar que no exista cita duplicada
        if self.repo.existe_cita(id_medico, fecha, hora):
            raise CitaDuplicadaError(
                f"Ya existe una cita para el médico {id_medico} "
                f"el {fecha} a las {hora}"
            )
        
        # Crear la cita
        cita = self.repo.create(
            id_paciente=id_paciente,
            id_medico=id_medico,
            fecha=fecha,
            hora=hora,
            motivo=motivo,
            observaciones=observaciones
        )
        
        # Crear notificaciones (esto también puede hacerse con trigger)
        self._crear_notificaciones_nueva_cita(cita)
        
        return cita
    
    def cancelar_cita(
        self,
        id_cita: int,
        motivo_cancelacion: str = None
    ) -> Cita:
        """
        Cancela una cita
        
        Reglas de negocio:
        - Solo se pueden cancelar citas AGENDADAS
        - Se registra el motivo de cancelación
        """
        cita = self.obtener_por_id(id_cita)
        
        if not cita.puede_cancelarse():
            raise CitaNoPuedeCancelarseError(
                f"La cita {id_cita} no puede cancelarse (estado: {cita.estado})"
            )
        
        # Actualizar estado
        cita_actualizada = self.repo.update_estado(
            id_cita,
            'CANCELADA',
            motivo_cancelacion
        )
        
        # Notificar cancelación
        self._notificar_cancelacion(cita_actualizada)
        
        return cita_actualizada
    
    def reprogramar_cita(
        self,
        id_cita: int,
        nueva_fecha: date,
        nueva_hora: time,
        motivo: str = None
    ) -> Cita:
        """
        Reprograma una cita
        
        Reglas de negocio:
        - Solo se pueden reprogramar citas AGENDADAS o REPROGRAMADAS
        - La nueva fecha/hora debe estar disponible
        - Debe cumplir todas las validaciones de una cita nueva
        """
        cita = self.obtener_por_id(id_cita)
        
        if not cita.puede_reprogramarse():
            raise CitaNoPuedeReprogramarseError(
                f"La cita {id_cita} no puede reprogramarse (estado: {cita.estado})"
            )
        
        # Validar nueva fecha/hora
        CitaValidator.validar_fecha_cita(nueva_fecha)
        CitaValidator.validar_hora_cita(nueva_hora)
        
        # Validar disponibilidad (excluyendo esta cita)
        self._validar_disponibilidad_medico(cita.id_medico, nueva_fecha, nueva_hora)
        
        if self.repo.existe_cita(cita.id_medico, nueva_fecha, nueva_hora, exclude_id=id_cita):
            raise CitaNoDisponibleError(
                f"El horario {nueva_fecha} {nueva_hora} no está disponible"
            )
        
        # Reprogramar
        cita_actualizada = self.repo.reprogramar(
            id_cita,
            nueva_fecha,
            nueva_hora,
            motivo
        )
        
        # Notificar reprogramación
        self._notificar_reprogramacion(cita_actualizada)
        
        return cita_actualizada
    
    def marcar_como_atendida(
        self,
        id_cita: int,
        observaciones: str = None
    ) -> Cita:
        """
        Marca una cita como atendida
        
        Reglas de negocio:
        - Solo se pueden atender citas AGENDADAS
        """
        cita = self.obtener_por_id(id_cita)
        
        if not cita.puede_atenderse():
            raise EstadoCitaInvalidoError(
                f"La cita {id_cita} no puede ser atendida (estado: {cita.estado})"
            )
        
        return self.repo.update_estado(id_cita, 'ATENDIDA', observaciones)
    
    def obtener_por_id(self, id_cita: int) -> Cita:
        """Obtiene una cita por ID"""
        cita = self.repo.find_by_id(id_cita, 'id_cita')
        if not cita:
            raise CitaNoEncontradaError(f"Cita {id_cita} no encontrada")
        return cita
    
    def obtener_citas_paciente(
        self,
        id_paciente: int,
        solo_activas: bool = False
    ) -> List[Cita]:
        """Obtiene todas las citas de un paciente"""
        return self.repo.find_by_paciente(id_paciente, solo_activas)
    
    def obtener_citas_medico(
        self,
        id_medico: int,
        solo_activas: bool = False
    ) -> List[Cita]:
        """Obtiene todas las citas de un médico"""
        return self.repo.find_by_medico(id_medico, solo_activas)
    
    def obtener_citas_fecha(
        self,
        fecha: date,
        id_medico: int = None
    ) -> List[Cita]:
        """Obtiene citas de una fecha específica"""
        return self.repo.find_by_fecha(fecha, id_medico, solo_activas=True)
    
    def obtener_proximas_citas(
        self,
        id_paciente: int = None,
        id_medico: int = None,
        limit: int = 10
    ) -> List[Cita]:
        """Obtiene las próximas citas"""
        return self.repo.find_proximas(id_paciente, id_medico, limit)
    
    def obtener_disponibilidad_medico(
        self,
        id_medico: int,
        fecha: date
    ) -> List[time]:
        """
        Obtiene horarios disponibles de un médico en una fecha
        
        Retorna lista de horas disponibles
        """
        # Obtener día de la semana (1=Lunes, 7=Domingo)
        dia_semana = fecha.isoweekday()
        
        # Obtener horarios del médico
        horarios = self.horario_repo.find_by_medico_dia(id_medico, dia_semana)
        
        if not horarios:
            return []
        
        # Obtener citas existentes
        citas_existentes = self.repo.find_by_fecha(fecha, id_medico, solo_activas=True)
        horas_ocupadas = {cita.hora for cita in citas_existentes}
        
        # Generar slots disponibles
        disponibles = []
        for horario in horarios:
            hora_actual = horario.hora_inicio
            while hora_actual < horario.hora_fin:
                if hora_actual not in horas_ocupadas:
                    disponibles.append(hora_actual)
                
                # Incrementar en 30 minutos
                minutos = hora_actual.hour * 60 + hora_actual.minute + 30
                hora_actual = time(minutos // 60, minutos % 60)
        
        return sorted(disponibles)
    
    def _validar_disponibilidad_medico(
        self,
        id_medico: int,
        fecha: date,
        hora: time
    ):
        """
        Valida que el médico tenga horario disponible
        
        Reglas:
        - El médico debe tener horario configurado para ese día
        - La hora debe estar dentro del horario
        """
        dia_semana = fecha.isoweekday()
        horarios = self.horario_repo.find_by_medico_dia(id_medico, dia_semana)
        
        if not horarios:
            raise FueraDeHorarioError(
                f"El médico no tiene horarios configurados para ese día"
            )
        
        # Verificar que la hora esté en algún horario
        en_horario = False
        for horario in horarios:
            if horario.esta_en_horario(hora):
                en_horario = True
                break
        
        if not en_horario:
            raise FueraDeHorarioError(
                f"La hora {hora} está fuera del horario del médico"
            )
    
    def _crear_notificaciones_nueva_cita(self, cita: Cita):
        """Crea notificaciones para paciente y médico"""
        # Notificar al paciente
        paciente = self.paciente_repo.find_by_id(cita.id_paciente, 'id_paciente')
        if paciente:
            self.notif_repo.create(
                id_usuario=paciente.id_usuario,
                tipo='CONFIRMACION',
                mensaje=f"Cita agendada para {cita.fecha} a las {cita.hora}"
            )
        
        # Notificar al médico
        medico = self.medico_repo.find_by_id(cita.id_medico, 'id_medico')
        if medico:
            self.notif_repo.create(
                id_usuario=medico.id_usuario,
                tipo='INFO',
                mensaje=f"Nueva cita agendada para {cita.fecha} a las {cita.hora}"
            )
    
    def _notificar_cancelacion(self, cita: Cita):
        """Notifica cancelación de cita"""
        paciente = self.paciente_repo.find_by_id(cita.id_paciente, 'id_paciente')
        if paciente:
            self.notif_repo.create(
                id_usuario=paciente.id_usuario,
                tipo='ALERTA',
                mensaje=f"Cita del {cita.fecha} a las {cita.hora} cancelada"
            )
    
    def _notificar_reprogramacion(self, cita: Cita):
        """Notifica reprogramación de cita"""
        paciente = self.paciente_repo.find_by_id(cita.id_paciente, 'id_paciente')
        if paciente:
            self.notif_repo.create(
                id_usuario=paciente.id_usuario,
                tipo='INFO',
                mensaje=f"Cita reprogramada para {cita.fecha} a las {cita.hora}"
            )
