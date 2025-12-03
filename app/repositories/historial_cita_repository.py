"""
Repository for HistorialCita operations
"""

from typing import List, Optional
from database import db
from models.historial_cita import HistorialCita


class HistorialCitaRepository:
    """Repository for managing HistorialCita entities"""
    
    def __init__(self):
        pass
    
    def find_by_cita(self, id_cita: int) -> List[HistorialCita]:
        """Get all history records for a specific appointment"""
        query = """
            SELECT id_historial, id_cita, estado_anterior, estado_nuevo, 
                   fecha_cambio, descripcion
            FROM historial_cita
            WHERE id_cita = %s
            ORDER BY fecha_cambio DESC
        """
        
        rows = db.execute_query(query, (id_cita,))
        return [HistorialCita.from_db_row(row) for row in rows]
    
    def find_by_id(self, id_historial: int) -> Optional[HistorialCita]:
        """Get a history record by ID"""
        query = """
            SELECT id_historial, id_cita, estado_anterior, estado_nuevo, 
                   fecha_cambio, descripcion
            FROM historial_cita
            WHERE id_historial = %s
        """
        
        rows = db.execute_query(query, (id_historial,))
        if rows:
            return HistorialCita.from_db_row(rows[0])
        return None
    
    def get_all(self, limit: int = 100) -> List[HistorialCita]:
        """Get all history records"""
        query = """
            SELECT id_historial, id_cita, estado_anterior, estado_nuevo, 
                   fecha_cambio, descripcion
            FROM historial_cita
            ORDER BY fecha_cambio DESC
            LIMIT %s
        """
        
        rows = db.execute_query(query, (limit,))
        return [HistorialCita.from_db_row(row) for row in rows]
