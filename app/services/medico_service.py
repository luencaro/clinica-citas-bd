"""
Servicio de Médico - Lógica de negocio
"""

from typing import List
from datetime import time

from models.medico import Medico
from models.usuario import Usuario
from models.horario_medico import HorarioMedico
from repositories.medico_repository import MedicoRepository
from repositories.horario_repository import HorarioRepository
from services.usuario_service import UsuarioService
from validators import MedicoValidator, HorarioValidator
from exceptions import (
    MedicoNoEncontradoError,
    RegistroProfesionalDuplicadoError,
    HorarioSuperposicionError
)


class MedicoService:
    """
    Servicio para gestionar médicos y sus horarios
    """
    
    def __init__(self):
        self.repo = MedicoRepository()
        self.horario_repo = HorarioRepository()
        self.usuario_service = UsuarioService()
    
    def crear_medico_completo(
        self,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        contraseña: str,
        id_especialidad: int,
        registro_profesional: str,
        descripcion: str = None,
        activo: bool = True
    ) -> tuple[Usuario, Medico]:
        """
        Crea un usuario Y un médico en una transacción
        
        Retorna tupla (usuario, medico)
        """
        # Validar datos del médico
        MedicoValidator.validar_creacion_medico(
            id_especialidad,
            registro_profesional,
            descripcion
        )
        
        # Verificar registro profesional único
        if self.repo.exists_registro_profesional(registro_profesional):
            raise RegistroProfesionalDuplicadoError(
                f"El registro profesional {registro_profesional} ya existe"
            )
        
        # Crear usuario con rol MEDICO
        usuario = self.usuario_service.crear_usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            contraseña=contraseña,
            rol='MEDICO',
            activo=activo
        )
        
        # Crear médico
        try:
            medico = self.repo.create(
                id_usuario=usuario.id_usuario,
                id_especialidad=id_especialidad,
                registro_profesional=registro_profesional,
                descripcion=descripcion,
                activo=activo
            )
            return usuario, medico
        except Exception as e:
            # Si falla, desactivar usuario
            self.usuario_service.desactivar_usuario(usuario.id_usuario)
            raise e
    
    def actualizar_medico(
        self,
        id_medico: int,
        id_especialidad: int = None,
        registro_profesional: str = None,
        descripcion: str = None,
        activo: bool = None
    ) -> Medico:
        """Actualiza datos del médico"""
        medico_actual = self.repo.find_by_id(id_medico, 'id_medico')
        if not medico_actual:
            raise MedicoNoEncontradoError(f"Médico {id_medico} no encontrado")
        
        # Validar registro profesional si cambió
        if (registro_profesional and 
            registro_profesional != medico_actual.registro_profesional):
            if self.repo.exists_registro_profesional(
                registro_profesional, 
                exclude_id=id_medico
            ):
                raise RegistroProfesionalDuplicadoError(
                    f"El registro {registro_profesional} ya existe"
                )
        
        return self.repo.update(
            id_medico=id_medico,
            id_especialidad=id_especialidad,
            registro_profesional=registro_profesional,
            descripcion=descripcion,
            activo=activo
        )
    
    def agregar_horario(
        self,
        id_medico: int,
        dia_semana: int,
        hora_inicio: time,
        hora_fin: time
    ) -> HorarioMedico:
        """
        Agrega un horario al médico
        
        Valida que no haya superposición
        """
        # Validar horario
        HorarioValidator.validar_horario(dia_semana, hora_inicio, hora_fin)
        
        # Validar superposición
        if self.horario_repo.tiene_superposicion(
            id_medico, dia_semana, hora_inicio, hora_fin
        ):
            raise HorarioSuperposicionError(
                f"El horario se superpone con otro existente"
            )
        
        return self.horario_repo.create(
            id_medico=id_medico,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
    
    def eliminar_horario(self, id_horario: int):
        """Elimina un horario"""
        self.horario_repo.delete(id_horario, 'id_horario')
    
    def obtener_por_id(self, id_medico: int) -> Medico:
        """Obtiene un médico por ID"""
        medico = self.repo.find_by_id(id_medico, 'id_medico')
        if not medico:
            raise MedicoNoEncontradoError(f"Médico {id_medico} no encontrado")
        return medico
    
    def obtener_por_especialidad(self, id_especialidad: int) -> List[Medico]:
        """Obtiene médicos por especialidad"""
        return self.repo.find_by_especialidad(id_especialidad)
    
    def obtener_horarios(self, id_medico: int) -> List[HorarioMedico]:
        """Obtiene todos los horarios de un médico"""
        return self.horario_repo.find_by_medico(id_medico)
    
    def listar_activos(self) -> List[Medico]:
        """Lista médicos activos"""
        return self.repo.find_activos()
    
    def listar_todos(self) -> List[Medico]:
        """Lista todos los médicos"""
        return self.repo.find_all()
