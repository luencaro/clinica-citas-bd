"""
Modelo de Horario Médico
"""

from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class HorarioMedico:
    """
    Representa un horario de disponibilidad de un médico
    """
    id_horario: Optional[int] = None
    id_medico: Optional[int] = None
    dia_semana: int = 1  # 1=Lunes, 7=Domingo
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    activo: bool = True
    
    DIAS_SEMANA = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miércoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Sábado',
        7: 'Domingo'
    }
    
    def __post_init__(self):
        """Validaciones al crear el objeto"""
        if not 1 <= self.dia_semana <= 7:
            raise ValueError(f"Día de semana inválido: {self.dia_semana}")
        
        if self.hora_inicio and self.hora_fin and self.hora_inicio >= self.hora_fin:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin")
    
    @property
    def nombre_dia(self) -> str:
        """Retorna el nombre del día de la semana"""
        return self.DIAS_SEMANA.get(self.dia_semana, 'Desconocido')
    
    def esta_en_horario(self, hora: time) -> bool:
        """Verifica si una hora está dentro del horario"""
        if not self.hora_inicio or not self.hora_fin:
            return False
        return self.hora_inicio <= hora < self.hora_fin
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario"""
        return {
            'id_horario': self.id_horario,
            'id_medico': self.id_medico,
            'dia_semana': self.dia_semana,
            'nombre_dia': self.nombre_dia,
            'hora_inicio': self.hora_inicio.isoformat() if self.hora_inicio else None,
            'hora_fin': self.hora_fin.isoformat() if self.hora_fin else None,
            'activo': self.activo
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'HorarioMedico':
        """Crea una instancia desde una fila de la BD"""
        return cls(
            id_horario=row[0],
            id_medico=row[1],
            dia_semana=row[2],
            hora_inicio=row[3],
            hora_fin=row[4],
            activo=row[5]
        )
