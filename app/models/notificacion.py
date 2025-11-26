"""
Modelo de Notificación
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Notificacion:
    """
    Representa una notificación del sistema
    """
    id_notificacion: Optional[int] = None
    id_usuario: Optional[int] = None
    tipo: str = "INFO"  # INFO, RECORDATORIO, ALERTA, CONFIRMACION
    mensaje: str = ""
    fecha_envio: Optional[datetime] = None
    leida: bool = False
    
    TIPOS_VALIDOS = ['INFO', 'RECORDATORIO', 'ALERTA', 'CONFIRMACION']
    
    def __post_init__(self):
        """Validaciones al crear el objeto"""
        if self.tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de notificación inválido: {self.tipo}")
    
    def marcar_como_leida(self):
        """Marca la notificación como leída"""
        self.leida = True
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_notificacion': self.id_notificacion,
            'id_usuario': self.id_usuario,
            'tipo': self.tipo,
            'mensaje': self.mensaje,
            'fecha_envio': self.fecha_envio.isoformat() if self.fecha_envio else None,
            'leida': self.leida
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Notificacion':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_notificacion=row[0],
            id_usuario=row[1],
            tipo=row[2],
            mensaje=row[3],
            fecha_envio=row[4],
            leida=row[5]
        )
