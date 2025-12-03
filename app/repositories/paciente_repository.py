"""
Repositorio de Paciente
"""

from typing import Optional
from datetime import date
from database import db
from models.paciente import Paciente
from .base_repository import BaseRepository


class PacienteRepository(BaseRepository[Paciente]):
    """Repositorio para operaciones con pacientes"""
    
    def __init__(self):
        super().__init__('paciente', Paciente)
    
    def create(
        self,
        id_usuario: int,
        fecha_nacimiento: date,
        direccion: str = None
    ) -> Paciente:
        """Crea un nuevo paciente"""
        query = """
            INSERT INTO paciente (id_usuario, fecha_nacimiento, direccion)
            VALUES (%s, %s, %s)
            RETURNING id_paciente, id_usuario, fecha_nacimiento, direccion
        """
        result = db.execute_query(
            query,
            (id_usuario, fecha_nacimiento, direccion),
            fetch='one'
        )
        return Paciente.from_db_row(result)
    
    def update(
        self,
        id_paciente: int,
        fecha_nacimiento: date = None,
        direccion: str = None
    ) -> Optional[Paciente]:
        """Actualiza un paciente"""
        updates = []
        params = []
        
        if fecha_nacimiento is not None:
            updates.append("fecha_nacimiento = %s")
            params.append(fecha_nacimiento)
        if direccion is not None:
            updates.append("direccion = %s")
            params.append(direccion)
        
        if not updates:
            return self.find_by_id(id_paciente, 'id_paciente')
        
        params.append(id_paciente)
        query = f"""
            UPDATE paciente 
            SET {', '.join(updates)}
            WHERE id_paciente = %s
            RETURNING id_paciente, id_usuario, fecha_nacimiento, direccion
        """
        
        result = db.execute_query(query, tuple(params), fetch='one')
        return Paciente.from_db_row(result) if result else None
    
    def find_by_usuario_id(self, id_usuario: int) -> Optional[Paciente]:
        """Busca paciente por ID de usuario"""
        query = "SELECT * FROM paciente WHERE id_usuario = %s"
        result = db.execute_query(query, (id_usuario,), fetch='one')
        return Paciente.from_db_row(result) if result else None
    
    def find_by_usuario(self, id_usuario: int) -> Optional[Paciente]:
        """Alias de find_by_usuario_id para compatibilidad"""
        return self.find_by_usuario_id(id_usuario)
