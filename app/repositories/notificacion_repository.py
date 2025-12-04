"""
Repositorio de Notificación
"""

from typing import List, Optional
from database import db
from models.notificacion import Notificacion
from .base_repository import BaseRepository


class NotificacionRepository(BaseRepository[Notificacion]):
    """Repositorio para operaciones con notificaciones"""
    
    def __init__(self):
        super().__init__('notificacion', Notificacion)
    
    def create(
        self,
        id_usuario: int,
        mensaje: str,
        tipo: str = "INFO"
    ) -> Notificacion:
        """Crea una nueva notificación"""
        query = """
            INSERT INTO notificacion (id_usuario, tipo, mensaje)
            VALUES (%s, %s, %s)
            RETURNING id_notificacion, id_usuario, tipo, mensaje, fecha_envio, leida
        """
        result = db.execute_query(query, (id_usuario, tipo, mensaje), fetch='one')
        return Notificacion.from_db_row(result)
    
    def marcar_leida(self, id_notificacion: int) -> Optional[Notificacion]:
        """Marca una notificación como leída"""
        query = """
            UPDATE notificacion 
            SET leida = TRUE
            WHERE id_notificacion = %s
            RETURNING id_notificacion, id_usuario, tipo, mensaje, fecha_envio, leida
        """
        result = db.execute_query(query, (id_notificacion,), fetch='one')
        return Notificacion.from_db_row(result) if result else None
    
    def marcar_como_leida(self, id_notificacion: int) -> Optional[Notificacion]:
        """Alias de marcar_leida para compatibilidad"""
        return self.marcar_leida(id_notificacion)
    
    def find_by_usuario(
        self,
        id_usuario: int,
        solo_no_leidas: bool = False,
        limit: int = 50
    ) -> List[Notificacion]:
        """Obtiene notificaciones de un usuario"""
        query = "SELECT * FROM notificacion WHERE id_usuario = %s"
        if solo_no_leidas:
            query += " AND leida = FALSE"
        query += f" ORDER BY fecha_envio DESC LIMIT {limit}"
        
        results = db.execute_query(query, (id_usuario,), fetch='all')
        return [Notificacion.from_db_row(row) for row in results]
    
    def count_no_leidas(self, id_usuario: int) -> int:
        """Cuenta notificaciones no leídas"""
        query = "SELECT COUNT(*) FROM notificacion WHERE id_usuario = %s AND leida = FALSE"
        result = db.execute_query(query, (id_usuario,), fetch='one')
        return result[0] if result else 0
    
    def marcar_todas_leidas(self, id_usuario: int) -> int:
        """Marca todas las notificaciones como leídas"""
        query = """
            UPDATE notificacion 
            SET leida = TRUE
            WHERE id_usuario = %s AND leida = FALSE
        """
        db.execute_query(query, (id_usuario,))
        return True
