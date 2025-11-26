"""
Repositorio de Especialidad
"""

from typing import List, Optional
from database import db
from models.especialidad import Especialidad
from .base_repository import BaseRepository


class EspecialidadRepository(BaseRepository[Especialidad]):
    """Repositorio para operaciones con especialidades"""
    
    def __init__(self):
        super().__init__('especialidad', Especialidad)
    
    def create(self, nombre: str, descripcion: str = None, activo: bool = True) -> Especialidad:
        """Crea una nueva especialidad"""
        query = """
            INSERT INTO especialidad (nombre, descripcion, activo)
            VALUES (%s, %s, %s)
            RETURNING id_especialidad, nombre, descripcion, activo
        """
        result = db.execute_query(query, (nombre, descripcion, activo), fetch='one')
        return Especialidad.from_db_row(result)
    
    def update(
        self,
        id_especialidad: int,
        nombre: str = None,
        descripcion: str = None,
        activo: bool = None
    ) -> Optional[Especialidad]:
        """Actualiza una especialidad"""
        updates = []
        params = []
        
        if nombre is not None:
            updates.append("nombre = %s")
            params.append(nombre)
        if descripcion is not None:
            updates.append("descripcion = %s")
            params.append(descripcion)
        if activo is not None:
            updates.append("activo = %s")
            params.append(activo)
        
        if not updates:
            return self.find_by_id(id_especialidad, 'id_especialidad')
        
        params.append(id_especialidad)
        query = f"""
            UPDATE especialidad 
            SET {', '.join(updates)}
            WHERE id_especialidad = %s
            RETURNING id_especialidad, nombre, descripcion, activo
        """
        
        result = db.execute_query(query, tuple(params), fetch='one')
        return Especialidad.from_db_row(result) if result else None
    
    def find_by_nombre(self, nombre: str) -> Optional[Especialidad]:
        """Busca especialidad por nombre"""
        query = "SELECT * FROM especialidad WHERE nombre = %s"
        result = db.execute_query(query, (nombre,), fetch='one')
        return Especialidad.from_db_row(result) if result else None
    
    def find_activas(self) -> List[Especialidad]:
        """Obtiene todas las especialidades activas"""
        query = "SELECT * FROM especialidad WHERE activo = TRUE ORDER BY nombre"
        results = db.execute_query(query, fetch='all')
        return [Especialidad.from_db_row(row) for row in results]
    
    def exists_nombre(self, nombre: str, exclude_id: int = None) -> bool:
        """Verifica si existe un nombre de especialidad"""
        if exclude_id:
            query = "SELECT 1 FROM especialidad WHERE nombre = %s AND id_especialidad != %s LIMIT 1"
            result = db.execute_query(query, (nombre, exclude_id), fetch='one')
        else:
            query = "SELECT 1 FROM especialidad WHERE nombre = %s LIMIT 1"
            result = db.execute_query(query, (nombre,), fetch='one')
        return result is not None
