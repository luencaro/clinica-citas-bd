"""
Servicio de Paciente - Lógica de negocio
"""

from typing import List
from datetime import date

from models.paciente import Paciente
from models.usuario import Usuario
from repositories.paciente_repository import PacienteRepository
from services.usuario_service import UsuarioService
from validators import PacienteValidator
from exceptions import (
    PacienteNoEncontradoError,
    PacienteDuplicadoError
)


class PacienteService:
    """
    Servicio para gestionar pacientes
    """
    
    def __init__(self):
        self.repo = PacienteRepository()
        self.usuario_service = UsuarioService()
    
    def crear_paciente_completo(
        self,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        contraseña: str,
        fecha_nacimiento: date,
        direccion: str = None,
        genero: str = None,
        observaciones_medicas: str = None
    ) -> tuple[Usuario, Paciente]:
        """
        Crea un usuario Y un paciente en una transacción
        
        Retorna tupla (usuario, paciente)
        """
        # Validar datos del paciente
        PacienteValidator.validar_creacion_paciente(
            fecha_nacimiento,
            direccion,
            genero,
            observaciones_medicas
        )
        
        # Crear usuario con rol PACIENTE
        usuario = self.usuario_service.crear_usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            contraseña=contraseña,
            rol='PACIENTE'
        )
        
        # Crear paciente
        try:
            paciente = self.repo.create(
                id_usuario=usuario.id_usuario,
                fecha_nacimiento=fecha_nacimiento,
                direccion=direccion,
                genero=genero,
                observaciones_medicas=observaciones_medicas
            )
            return usuario, paciente
        except Exception as e:
            # Si falla la creación del paciente, desactivar usuario
            self.usuario_service.desactivar_usuario(usuario.id_usuario)
            raise e
    
    def actualizar_datos_paciente(
        self,
        id_paciente: int,
        fecha_nacimiento: date = None,
        direccion: str = None,
        genero: str = None,
        observaciones_medicas: str = None
    ) -> Paciente:
        """Actualiza datos específicos del paciente"""
        if not self.repo.exists(id_paciente, 'id_paciente'):
            raise PacienteNoEncontradoError(f"Paciente {id_paciente} no encontrado")
        
        return self.repo.update(
            id_paciente=id_paciente,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
            genero=genero,
            observaciones_medicas=observaciones_medicas
        )
    
    def obtener_por_id(self, id_paciente: int) -> Paciente:
        """Obtiene un paciente por ID"""
        paciente = self.repo.find_by_id(id_paciente, 'id_paciente')
        if not paciente:
            raise PacienteNoEncontradoError(f"Paciente {id_paciente} no encontrado")
        return paciente
    
    def obtener_por_usuario(self, id_usuario: int) -> Paciente:
        """Obtiene un paciente por su ID de usuario"""
        paciente = self.repo.find_by_usuario_id(id_usuario)
        if not paciente:
            raise PacienteNoEncontradoError(
                f"No existe paciente para usuario {id_usuario}"
            )
        return paciente
    
    def listar_todos(self) -> List[Paciente]:
        """Lista todos los pacientes"""
        return self.repo.find_all()
