"""
Repositorio de Médico
"""

from typing import List, Optional
from database import db
from models.medico import Medico
from .base_repository import BaseRepository


class MedicoRepository(BaseRepository[Medico]):
    """Repositorio para operaciones con médicos"""
    
    def __init__(self):
        super().__init__('medico', Medico)
    
    def create(
        self,
        id_usuario: int,
        id_especialidad: int,
        registro_profesional: str,
        activo: bool = True
    ) -> Medico:
        """Crea un nuevo médico"""
        query = """
            INSERT INTO medico (id_usuario, id_especialidad, registro_profesional, activo)
            VALUES (%s, %s, %s, %s)
            RETURNING id_medico, id_usuario, id_especialidad, registro_profesional, activo
        """
        result = db.execute_query(
            query,
            (id_usuario, id_especialidad, registro_profesional, activo),
            fetch='one'
        )
        return Medico.from_db_row(result)
    
    def update(
        self,
        id_medico: int,
        id_especialidad: int = None,
        registro_profesional: str = None,
        activo: bool = None
    ) -> Optional[Medico]:
        """Actualiza un médico"""
        updates = []
        params = []
        
        if id_especialidad is not None:
            updates.append("id_especialidad = %s")
            params.append(id_especialidad)
        if registro_profesional is not None:
            updates.append("registro_profesional = %s")
            params.append(registro_profesional)
        if activo is not None:
            updates.append("activo = %s")
            params.append(activo)
        
        if not updates:
            return self.find_by_id(id_medico, 'id_medico')
        
        params.append(id_medico)
        query = f"""
            UPDATE medico 
            SET {', '.join(updates)}
            WHERE id_medico = %s
            RETURNING id_medico, id_usuario, id_especialidad, registro_profesional, activo
        """
        
        result = db.execute_query(query, tuple(params), fetch='one')
        return Medico.from_db_row(result) if result else None
    
    def find_by_usuario_id(self, id_usuario: int) -> Optional[Medico]:
        """Busca médico por ID de usuario"""
        query = "SELECT * FROM medico WHERE id_usuario = %s"
        result = db.execute_query(query, (id_usuario,), fetch='one')
        return Medico.from_db_row(result) if result else None
    
    def find_by_especialidad(self, id_especialidad: int, solo_activos: bool = True) -> List[Medico]:
        """Busca médicos por especialidad"""
        query = "SELECT * FROM medico WHERE id_especialidad = %s"
        if solo_activos:
            query += " AND activo = TRUE"
        
        results = db.execute_query(query, (id_especialidad,), fetch='all')
        return [Medico.from_db_row(row) for row in results]
    
    def find_activos(self) -> List[Medico]:
        """Obtiene todos los médicos activos"""
        query = "SELECT * FROM medico WHERE activo = TRUE"
        results = db.execute_query(query, fetch='all')
        return [Medico.from_db_row(row) for row in results]
    
    def exists_registro_profesional(self, registro: str, exclude_id: int = None) -> bool:
        """Verifica si existe un registro profesional"""
        if exclude_id:
            query = "SELECT 1 FROM medico WHERE registro_profesional = %s AND id_medico != %s LIMIT 1"
            result = db.execute_query(query, (registro, exclude_id), fetch='one')
        else:
            query = "SELECT 1 FROM medico WHERE registro_profesional = %s LIMIT 1"
            result = db.execute_query(query, (registro,), fetch='one')
        return result is not None
