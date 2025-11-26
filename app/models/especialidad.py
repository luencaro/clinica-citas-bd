"""
Modelo de Especialidad
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Especialidad:
    """
    Representa una especialidad médica
    """
    id_especialidad: Optional[int] = None
    nombre: str = ""
    descripcion: Optional[str] = None
    activo: bool = True
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_especialidad': self.id_especialidad,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Especialidad':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_especialidad=row[0],
            nombre=row[1],
            descripcion=row[2],
            activo=row[3]
        )
