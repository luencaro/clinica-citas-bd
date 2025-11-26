"""
Modelo de Médico
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Medico:
    """
    Representa un médico del sistema
    """
    id_medico: Optional[int] = None
    id_usuario: Optional[int] = None
    id_especialidad: Optional[int] = None
    registro_profesional: str = ""
    activo: bool = True
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_medico': self.id_medico,
            'id_usuario': self.id_usuario,
            'id_especialidad': self.id_especialidad,
            'registro_profesional': self.registro_profesional,
            'activo': self.activo
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Medico':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_medico=row[0],
            id_usuario=row[1],
            id_especialidad=row[2],
            registro_profesional=row[3],
            activo=row[4]
        )
