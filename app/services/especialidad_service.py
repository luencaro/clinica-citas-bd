"""
Servicio de Especialidad - Lógica de negocio
"""

from typing import List

from models.especialidad import Especialidad
from repositories.especialidad_repository import EspecialidadRepository
from exceptions import (
    EspecialidadNoEncontradaError,
    EspecialidadDuplicadaError
)


class EspecialidadService:
    """
    Servicio para gestionar especialidades médicas
    """
    
    def __init__(self):
        self.repo = EspecialidadRepository()
    
    def crear_especialidad(
        self,
        nombre: str,
        descripcion: str = None,
        activa: bool = True
    ) -> Especialidad:
        """
        Crea una nueva especialidad
        
        El nombre debe ser único
        """
        # Validar nombre único
        if self.repo.exists_nombre(nombre):
            raise EspecialidadDuplicadaError(
                f"La especialidad '{nombre}' ya existe"
            )
        
        return self.repo.create(
            nombre=nombre,
            descripcion=descripcion,
            activa=activa
        )
    
    def actualizar_especialidad(
        self,
        id_especialidad: int,
        nombre: str = None,
        descripcion: str = None,
        activa: bool = None
    ) -> Especialidad:
        """Actualiza una especialidad"""
        especialidad_actual = self.repo.find_by_id(id_especialidad, 'id_especialidad')
        if not especialidad_actual:
            raise EspecialidadNoEncontradaError(
                f"Especialidad {id_especialidad} no encontrada"
            )
        
        # Validar nombre único si cambió
        if nombre and nombre != especialidad_actual.nombre:
            if self.repo.exists_nombre(nombre, exclude_id=id_especialidad):
                raise EspecialidadDuplicadaError(
                    f"La especialidad '{nombre}' ya existe"
                )
        
        return self.repo.update(
            id_especialidad=id_especialidad,
            nombre=nombre,
            descripcion=descripcion,
            activa=activa
        )
    
    def obtener_por_id(self, id_especialidad: int) -> Especialidad:
        """Obtiene una especialidad por ID"""
        especialidad = self.repo.find_by_id(id_especialidad, 'id_especialidad')
        if not especialidad:
            raise EspecialidadNoEncontradaError(
                f"Especialidad {id_especialidad} no encontrada"
            )
        return especialidad
    
    def obtener_por_nombre(self, nombre: str) -> Especialidad:
        """Obtiene una especialidad por nombre"""
        especialidad = self.repo.find_by_nombre(nombre)
        if not especialidad:
            raise EspecialidadNoEncontradaError(
                f"Especialidad '{nombre}' no encontrada"
            )
        return especialidad
    
    def listar_activas(self) -> List[Especialidad]:
        """Lista especialidades activas"""
        return self.repo.find_activas()
    
    def listar_todas(self) -> List[Especialidad]:
        """Lista todas las especialidades"""
        return self.repo.find_all()
    
    def activar(self, id_especialidad: int) -> Especialidad:
        """Activa una especialidad"""
        return self.actualizar_especialidad(id_especialidad, activa=True)
    
    def desactivar(self, id_especialidad: int) -> Especialidad:
        """Desactiva una especialidad"""
        return self.actualizar_especialidad(id_especialidad, activa=False)
