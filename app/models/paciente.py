"""
Modelo de Paciente
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Paciente:
    """
    Representa un paciente del sistema
    """
    id_paciente: Optional[int] = None
    id_usuario: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    
    @property
    def edad(self) -> int:
        """Calcula la edad del paciente"""
        if not self.fecha_nacimiento:
            return 0
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def es_mayor_de_edad(self) -> bool:
        """Verifica si el paciente es mayor de edad"""
        return self.edad >= 18
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_paciente': self.id_paciente,
            'id_usuario': self.id_usuario,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'direccion': self.direccion,
            'edad': self.edad
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Paciente':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_paciente=row[0],
            id_usuario=row[1],
            fecha_nacimiento=row[2],
            direccion=row[3]
        )
