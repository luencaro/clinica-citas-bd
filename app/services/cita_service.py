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
        Agenda una nueva cita usando STORED PROCEDURE sp_agendar_cita
        
        Reglas de negocio:
        1. Paciente debe existir
        2. Médico debe existir y estar activo
        3. Fecha debe ser futura
        4. Hora debe estar en horario del médico
        5. No debe existir otra cita en ese horario
        6. Motivo debe ser válido
        
        NOTA: Usa stored procedure que implementa todas las validaciones en PostgreSQL
        """
        # Validar datos básicos en backend
        CitaValidator.validar_motivo(motivo)
        
        # Validar paciente existe
        paciente = self.paciente_repo.find_by_id(id_paciente, 'id_paciente')
        if not paciente:
            raise PacienteNoEncontradoError(f"Paciente {id_paciente} no encontrado")
        
        # Validar médico existe y está activo
        medico = self.medico_repo.find_by_id(id_medico, 'id_medico')
        if not medico:
            raise MedicoNoEncontradoError(f"Médico {id_medico} no encontrado")
        
        if not medico.activo:
            raise MedicoInactivoError(f"El médico {id_medico} no está activo")
        
        # Verificar que el paciente no tenga otra cita a la misma hora
        if self.repo.existe_cita_paciente(id_paciente, fecha, hora):
            raise CitaDuplicadaError(
                f"El paciente ya tiene una cita agendada "
                f"el {fecha} a las {hora}"
            )
        
        # USAR STORED PROCEDURE para agendar la cita
        # El procedure valida disponibilidad, horarios, y crea la cita
        try:
            from database import db
            query = """
                SELECT sp_agendar_cita(%s, %s, %s, %s, %s, %s) AS id_cita
            """
            result = db.execute_query(
                query,
                (id_paciente, id_medico, fecha, hora, motivo, observaciones),
                fetch='one'
            )
            
            if not result:
                raise CitaNoDisponibleError("No se pudo agendar la cita")
            
            id_cita = result[0]
            
            # Recuperar la cita creada
            cita = self.repo.find_by_id(id_cita, 'id_cita')
            return cita
            
        except Exception as e:
            # El stored procedure lanza excepciones descriptivas
            error_msg = str(e)
            if "fecha debe ser futura" in error_msg.lower() or "fecha no puede ser pasada" in error_msg.lower():
                raise FechaPasadaError("La fecha de la cita no puede ser en el pasado")
            elif "hora debe ser futura" in error_msg.lower():
                raise FechaPasadaError("La hora de la cita debe ser futura (no puede ser para hoy en una hora que ya pasó)")
            elif "no está disponible" in error_msg.lower():
                # Proporcionar información adicional sobre disponibilidad
                dia_semana = fecha.weekday() + 1  # Python: 0=Lun, PostgreSQL: 1=Lun
                horarios = self.horario_repo.find_by_medico(id_medico)
                tiene_horario_ese_dia = any(h.dia_semana == dia_semana for h in horarios)
                
                if not tiene_horario_ese_dia:
                    dias = {1: 'lunes', 2: 'martes', 3: 'miércoles', 4: 'jueves', 5: 'viernes', 6: 'sábado', 7: 'domingo'}
                    raise CitaNoDisponibleError(
                        f"El médico seleccionado no trabaja los {dias[dia_semana]}. "
                        f"Por favor, selecciona otro día."
                    )
                
                # Verificar si hay conflicto de horario
                citas_existentes = self.repo.find_by_fecha(fecha, id_medico)
                if any(c.hora == hora and c.estado not in ['CANCELADA', 'NO_ASISTIO'] for c in citas_existentes):
                    raise CitaNoDisponibleError(
                        f"Ya existe una cita agendada para ese médico el {fecha} a las {hora}. "
                        f"Por favor, selecciona otra hora."
                    )
                
                raise CitaNoDisponibleError(
                    f"El horario seleccionado no está disponible. La hora debe estar dentro del horario laboral del médico."
                )
            else:
                raise CitaNoDisponibleError(f"Error al agendar cita: {error_msg}")
    
    def cancelar_cita(
        self,
        id_cita: int,
        motivo_cancelacion: str = None
    ) -> Cita:
        """
        Cancela una cita usando STORED PROCEDURE sp_cancelar_cita
        
        Reglas de negocio:
        - Solo se pueden cancelar citas AGENDADAS
        - Se registra el motivo de cancelación
        
        NOTA: Usa stored procedure que valida estados y crea historial automáticamente
        """
        # Verificar que la cita existe antes de llamar al procedure
        cita = self.obtener_por_id(id_cita)
        
        # USAR STORED PROCEDURE para cancelar
        # El procedure valida el estado y actualiza con triggers
        try:
            from database import db
            query = """
                SELECT sp_cancelar_cita(%s, %s)
            """
            db.execute_query(
                query,
                (id_cita, motivo_cancelacion),
                fetch='one'
            )
            
            # Recuperar la cita actualizada
            cita_actualizada = self.repo.find_by_id(id_cita, 'id_cita')
            return cita_actualizada
            
        except Exception as e:
            error_msg = str(e)
            if "no puede cancelarse" in error_msg.lower() or "solo se pueden cancelar" in error_msg.lower():
                raise CitaNoPuedeCancelarseError(error_msg)
            else:
                raise CitaNoPuedeCancelarseError(f"Error al cancelar cita: {error_msg}")
    
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
        - Solo se pueden atender citas AGENDADAS o REPROGRAMADAS
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
