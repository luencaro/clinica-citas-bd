"""
Repositorio de Cita
"""

from typing import List, Optional
from datetime import date, time, datetime
from database import db
from models.cita import Cita
from .base_repository import BaseRepository


class CitaRepository(BaseRepository[Cita]):
    """Repositorio para operaciones con citas"""
    
    def __init__(self):
        super().__init__('cita', Cita)
    
    def create(
        self,
        id_paciente: int,
        id_medico: int,
        fecha: date,
        hora: time,
        motivo: str,
        observaciones: str = None
    ) -> Cita:
        """Crea una nueva cita"""
        query = """
            INSERT INTO cita (id_paciente, id_medico, fecha, hora, motivo, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_cita, id_paciente, id_medico, fecha, hora, motivo, estado, observaciones, fecha_creacion
        """
        result = db.execute_query(
            query,
            (id_paciente, id_medico, fecha, hora, motivo, observaciones),
            fetch='one'
        )
        return Cita.from_db_row(result)
    
    def update_estado(
        self,
        id_cita: int,
        nuevo_estado: str,
        observaciones: str = None
    ) -> Optional[Cita]:
        """Actualiza el estado de una cita"""
        if observaciones:
            query = """
                UPDATE cita 
                SET estado = %s, observaciones = %s
                WHERE id_cita = %s
                RETURNING id_cita, id_paciente, id_medico, fecha, hora, motivo, estado, observaciones, fecha_creacion
            """
            params = (nuevo_estado, observaciones, id_cita)
        else:
            query = """
                UPDATE cita 
                SET estado = %s
                WHERE id_cita = %s
                RETURNING id_cita, id_paciente, id_medico, fecha, hora, motivo, estado, observaciones, fecha_creacion
            """
            params = (nuevo_estado, id_cita)
        
        result = db.execute_query(query, params, fetch='one')
        return Cita.from_db_row(result) if result else None
    
    def reprogramar(
        self,
        id_cita: int,
        nueva_fecha: date,
        nueva_hora: time,
        observaciones: str = None
    ) -> Optional[Cita]:
        """Reprograma una cita"""
        if observaciones:
            query = """
                UPDATE cita 
                SET fecha = %s, hora = %s, estado = 'REPROGRAMADA', observaciones = %s
                WHERE id_cita = %s
                RETURNING id_cita, id_paciente, id_medico, fecha, hora, motivo, estado, observaciones, fecha_creacion
            """
            params = (nueva_fecha, nueva_hora, observaciones, id_cita)
        else:
            query = """
                UPDATE cita 
                SET fecha = %s, hora = %s, estado = 'REPROGRAMADA'
                WHERE id_cita = %s
                RETURNING id_cita, id_paciente, id_medico, fecha, hora, motivo, estado, observaciones, fecha_creacion
            """
            params = (nueva_fecha, nueva_hora, id_cita)
        
        result = db.execute_query(query, params, fetch='one')
        return Cita.from_db_row(result) if result else None
    
    def find_by_paciente(
        self,
        id_paciente: int,
        solo_activas: bool = False
    ) -> List[Cita]:
        """Obtiene citas de un paciente"""
        query = "SELECT * FROM cita WHERE id_paciente = %s"
        if solo_activas:
            query += " AND estado IN ('AGENDADA', 'REPROGRAMADA')"
        query += " ORDER BY fecha DESC, hora DESC"
        
        results = db.execute_query(query, (id_paciente,), fetch='all')
        return [Cita.from_db_row(row) for row in results]
    
    def find_by_medico(
        self,
        id_medico: int,
        solo_activas: bool = False
    ) -> List[Cita]:
        """Obtiene citas de un médico"""
        query = "SELECT * FROM cita WHERE id_medico = %s"
        if solo_activas:
            query += " AND estado IN ('AGENDADA', 'REPROGRAMADA')"
        query += " ORDER BY fecha DESC, hora DESC"
        
        results = db.execute_query(query, (id_medico,), fetch='all')
        return [Cita.from_db_row(row) for row in results]
    
    def find_by_fecha(
        self,
        fecha: date,
        id_medico: int = None,
        solo_activas: bool = False
    ) -> List[Cita]:
        """Obtiene citas de una fecha específica"""
        query = "SELECT * FROM cita WHERE fecha = %s"
        params = [fecha]
        
        if id_medico:
            query += " AND id_medico = %s"
            params.append(id_medico)
        
        if solo_activas:
            query += " AND estado IN ('AGENDADA', 'REPROGRAMADA')"
        
        query += " ORDER BY hora"
        
        results = db.execute_query(query, tuple(params), fetch='all')
        return [Cita.from_db_row(row) for row in results]
    
    def find_proximas(
        self,
        id_paciente: int = None,
        id_medico: int = None,
        limit: int = 10
    ) -> List[Cita]:
        """Obtiene próximas citas"""
        query = """
            SELECT * FROM cita 
            WHERE fecha >= CURRENT_DATE 
            AND estado IN ('AGENDADA', 'REPROGRAMADA')
        """
        params = []
        
        if id_paciente:
            query += " AND id_paciente = %s"
            params.append(id_paciente)
        
        if id_medico:
            query += " AND id_medico = %s"
            params.append(id_medico)
        
        query += f" ORDER BY fecha, hora LIMIT {limit}"
        
        results = db.execute_query(query, tuple(params) if params else None, fetch='all')
        return [Cita.from_db_row(row) for row in results]
    
    def existe_cita(
        self,
        id_medico: int,
        fecha: date,
        hora: time,
        exclude_id: int = None
    ) -> bool:
        """Verifica si existe una cita en ese horario"""
        query = """
            SELECT 1 FROM cita 
            WHERE id_medico = %s 
            AND fecha = %s 
            AND hora = %s
            AND estado NOT IN ('CANCELADA')
        """
        params = [id_medico, fecha, hora]
        
        if exclude_id:
            query += " AND id_cita != %s"
            params.append(exclude_id)
        
        query += " LIMIT 1"
        result = db.execute_query(query, tuple(params), fetch='one')
        return result is not None
    
    def existe_cita_paciente(
        self,
        id_paciente: int,
        fecha: date,
        hora: time,
        exclude_id: int = None
    ) -> bool:
        """Verifica si el paciente ya tiene una cita en ese horario"""
        query = """
            SELECT 1 FROM cita 
            WHERE id_paciente = %s 
            AND fecha = %s 
            AND hora = %s
            AND estado NOT IN ('CANCELADA')
        """
        params = [id_paciente, fecha, hora]
        
        if exclude_id:
            query += " AND id_cita != %s"
            params.append(exclude_id)
        
        query += " LIMIT 1"
        result = db.execute_query(query, tuple(params), fetch='one')
        return result is not None
    
    def count_by_estado(self, estado: str) -> int:
        """Cuenta citas por estado"""
        query = "SELECT COUNT(*) FROM cita WHERE estado = %s"
        result = db.execute_query(query, (estado,), fetch='one')
        return result[0] if result else 0
