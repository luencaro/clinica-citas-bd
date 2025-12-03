"""
Modelo de Cita
"""

from dataclasses import dataclass
from datetime import date, time, datetime
from typing import Optional


@dataclass
class Cita:
    """
    Representa una cita médica
    """
    id_cita: Optional[int] = None
    id_paciente: Optional[int] = None
    id_medico: Optional[int] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None
    motivo: str = ""
    estado: str = "AGENDADA"  # AGENDADA, CANCELADA, REPROGRAMADA, ATENDIDA
    observaciones: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    
    ESTADOS_VALIDOS = ['AGENDADA', 'CANCELADA', 'REPROGRAMADA', 'ATENDIDA']
    
    def __post_init__(self):
        """Validaciones al crear el objeto"""
        if self.estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {self.estado}")
    
    def puede_cancelarse(self) -> bool:
        """Verifica si la cita puede ser cancelada"""
        return self.estado in ['AGENDADA', 'REPROGRAMADA']
    
    def puede_reprogramarse(self) -> bool:
        """Verifica si la cita puede ser reprogramada"""
        return self.estado in ['AGENDADA', 'REPROGRAMADA']
    
    def puede_atenderse(self) -> bool:
        """Verifica si la cita puede ser atendida"""
        return self.estado in ['AGENDADA', 'REPROGRAMADA']
    
    def esta_pendiente(self) -> bool:
        """Verifica si la cita está pendiente"""
        return self.estado == 'AGENDADA'
    
    def esta_completada(self) -> bool:
        """Verifica si la cita fue completada"""
        return self.estado == 'ATENDIDA'
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_cita': self.id_cita,
            'id_paciente': self.id_paciente,
            'id_medico': self.id_medico,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'hora': self.hora.isoformat() if self.hora else None,
            'motivo': self.motivo,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Cita':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_cita=row[0],
            id_paciente=row[1],
            id_medico=row[2],
            fecha=row[3],
            hora=row[4],
            motivo=row[5],
            estado=row[6],
            observaciones=row[7],
            fecha_creacion=row[8]
        )
