"""
Modelo de Usuario
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    """
    Representa un usuario del sistema (Admin, Médico o Paciente)
    """
    id_usuario: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    telefono: str = ""
    contraseña: str = ""
    rol: str = "PACIENTE"  # ADMIN, MEDICO, PACIENTE
    fecha_creacion: Optional[datetime] = None
    activo: bool = True
    
    def __post_init__(self):
        """Validaciones básicas al crear el objeto"""
        if self.rol not in ['ADMIN', 'MEDICO', 'PACIENTE']:
            raise ValueError(f"Rol inválido: {self.rol}")
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    def es_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self.rol == 'ADMIN'
    
    def es_medico(self) -> bool:
        """Verifica si el usuario es médico"""
        return self.rol == 'MEDICO'
    
    def es_paciente(self) -> bool:
        """Verifica si el usuario es paciente"""
        return self.rol == 'PACIENTE'
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'rol': self.rol,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'activo': self.activo
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Usuario':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_usuario=row[0],
            nombre=row[1],
            apellido=row[2],
            email=row[3],
            telefono=row[4],
            contraseña=row[5],
            rol=row[6],
            fecha_creacion=row[7],
            activo=row[8]
        )
