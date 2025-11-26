"""
Repositorio de Horario Médico
"""

from typing import List, Optional
from datetime import time
from database import db
from models.horario_medico import HorarioMedico
from .base_repository import BaseRepository


class HorarioRepository(BaseRepository[HorarioMedico]):
    """Repositorio para operaciones con horarios de médicos"""
    
    def __init__(self):
        super().__init__('horario_medico', HorarioMedico)
    
    def create(
        self,
        id_medico: int,
        dia_semana: int,
        hora_inicio: time,
        hora_fin: time,
        activo: bool = True
    ) -> HorarioMedico:
        """Crea un nuevo horario"""
        query = """
            INSERT INTO horario_medico (id_medico, dia_semana, hora_inicio, hora_fin, activo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_horario, id_medico, dia_semana, hora_inicio, hora_fin, activo
        """
        result = db.execute_query(
            query,
            (id_medico, dia_semana, hora_inicio, hora_fin, activo),
            fetch='one'
        )
        return HorarioMedico.from_db_row(result)
    
    def update(
        self,
        id_horario: int,
        dia_semana: int = None,
        hora_inicio: time = None,
        hora_fin: time = None,
        activo: bool = None
    ) -> Optional[HorarioMedico]:
        """Actualiza un horario"""
        updates = []
        params = []
        
        if dia_semana is not None:
            updates.append("dia_semana = %s")
            params.append(dia_semana)
        if hora_inicio is not None:
            updates.append("hora_inicio = %s")
            params.append(hora_inicio)
        if hora_fin is not None:
            updates.append("hora_fin = %s")
            params.append(hora_fin)
        if activo is not None:
            updates.append("activo = %s")
            params.append(activo)
        
        if not updates:
            return self.find_by_id(id_horario, 'id_horario')
        
        params.append(id_horario)
        query = f"""
            UPDATE horario_medico 
            SET {', '.join(updates)}
            WHERE id_horario = %s
            RETURNING id_horario, id_medico, dia_semana, hora_inicio, hora_fin, activo
        """
        
        result = db.execute_query(query, tuple(params), fetch='one')
        return HorarioMedico.from_db_row(result) if result else None
    
    def find_by_medico(self, id_medico: int, solo_activos: bool = True) -> List[HorarioMedico]:
        """Obtiene horarios de un médico"""
        query = "SELECT * FROM horario_medico WHERE id_medico = %s"
        if solo_activos:
            query += " AND activo = TRUE"
        query += " ORDER BY dia_semana, hora_inicio"
        
        results = db.execute_query(query, (id_medico,), fetch='all')
        return [HorarioMedico.from_db_row(row) for row in results]
    
    def find_by_medico_dia(self, id_medico: int, dia_semana: int) -> List[HorarioMedico]:
        """Obtiene horarios de un médico en un día específico"""
        query = """
            SELECT * FROM horario_medico 
            WHERE id_medico = %s AND dia_semana = %s AND activo = TRUE
            ORDER BY hora_inicio
        """
        results = db.execute_query(query, (id_medico, dia_semana), fetch='all')
        return [HorarioMedico.from_db_row(row) for row in results]
    
    def tiene_superposicion(
        self,
        id_medico: int,
        dia_semana: int,
        hora_inicio: time,
        hora_fin: time,
        exclude_id: int = None
    ) -> bool:
        """
        Verifica si hay superposición de horarios
        """
        query = """
            SELECT 1 FROM horario_medico
            WHERE id_medico = %s 
            AND dia_semana = %s
            AND activo = TRUE
            AND (
                (hora_inicio < %s AND hora_fin > %s) OR
                (hora_inicio < %s AND hora_fin > %s) OR
                (hora_inicio >= %s AND hora_fin <= %s)
            )
        """
        params = [
            id_medico, dia_semana,
            hora_fin, hora_inicio,  # Se superpone al inicio
            hora_fin, hora_fin,      # Se superpone al final
            hora_inicio, hora_fin    # Está contenido completamente
        ]
        
        if exclude_id:
            query += " AND id_horario != %s"
            params.append(exclude_id)
        
        query += " LIMIT 1"
        result = db.execute_query(query, tuple(params), fetch='one')
        return result is not None
