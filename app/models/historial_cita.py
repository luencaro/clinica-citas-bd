"""
Modelo de Historial de Cita
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class HistorialCita:
    """
    Representa un registro de cambio de estado de una cita
    """
    id_historial: Optional[int] = None
    id_cita: Optional[int] = None
    estado_anterior: Optional[str] = None
    estado_nuevo: str = ""
    fecha_cambio: Optional[datetime] = None
    descripcion: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_historial': self.id_historial,
            'id_cita': self.id_cita,
            'estado_anterior': self.estado_anterior,
            'estado_nuevo': self.estado_nuevo,
            'fecha_cambio': self.fecha_cambio.isoformat() if self.fecha_cambio else None,
            'descripcion': self.descripcion
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'HistorialCita':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_historial=row[0],
            id_cita=row[1],
            estado_anterior=row[2],
            estado_nuevo=row[3],
            fecha_cambio=row[4],
            descripcion=row[5]
        )
