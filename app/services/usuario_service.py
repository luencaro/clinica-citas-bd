"""
Servicio de Usuario - Lógica de negocio
"""

import bcrypt
from typing import List, Optional

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from validators import UsuarioValidator
from exceptions import (
    EmailDuplicadoError,
    TelefonoDuplicadoError,
    UsuarioNoEncontradoError,
    CredencialesInvalidasError
)


class UsuarioService:
    """
    Servicio para gestionar usuarios
    Implementa todas las reglas de negocio relacionadas con usuarios
    """
    
    def __init__(self):
        self.repo = UsuarioRepository()
    
    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        contraseña: str,
        rol: str,
        activo: bool = True
    ) -> Usuario:
        """
        Crea un nuevo usuario con validaciones completas
        
        Reglas de negocio:
        - Email debe ser único
        - Teléfono debe ser único
        - Contraseña debe cumplir requisitos de seguridad
        - Contraseña se guarda hasheada con bcrypt
        """
        # Validar datos
        UsuarioValidator.validar_creacion_usuario(
            nombre, apellido, email, telefono, contraseña, rol
        )
        
        # Verificar unicidad de email
        if self.repo.exists_email(email):
            raise EmailDuplicadoError(f"El email {email} ya está registrado")
        
        # Verificar unicidad de teléfono
        if self.repo.exists_telefono(telefono):
            raise TelefonoDuplicadoError(f"El teléfono {telefono} ya está registrado")
        
        # Hashear contraseña
        contraseña_hash = self._hashear_contraseña(contraseña)
        
        # Crear usuario
        usuario = self.repo.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            contraseña=contraseña_hash,
            rol=rol,
            activo=activo
        )
        
        return usuario
    
    def actualizar_usuario(
        self,
        id_usuario: int,
        nombre: str = None,
        apellido: str = None,
        email: str = None,
        telefono: str = None,
        contraseña: str = None,
        rol: str = None,
        activo: bool = None
    ) -> Usuario:
        """Actualiza un usuario existente"""
        # Verificar que existe
        usuario_actual = self.repo.find_by_id(id_usuario)
        if not usuario_actual:
            raise UsuarioNoEncontradoError(f"Usuario {id_usuario} no encontrado")
        
        # Validar email si cambió
        if email and email != usuario_actual.email:
            if self.repo.exists_email(email, exclude_id=id_usuario):
                raise EmailDuplicadoError(f"El email {email} ya está registrado")
        
        # Validar teléfono si cambió
        if telefono and telefono != usuario_actual.telefono:
            if self.repo.exists_telefono(telefono, exclude_id=id_usuario):
                raise TelefonoDuplicadoError(f"El teléfono {telefono} ya está registrado")
        
        # Hashear contraseña si se proporcionó
        if contraseña:
            contraseña = self._hashear_contraseña(contraseña)
        
        # Actualizar
        usuario = self.repo.update(
            id_usuario=id_usuario,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            contraseña=contraseña,
            rol=rol,
            activo=activo
        )
        
        return usuario
    
    def obtener_por_id(self, id_usuario: int) -> Usuario:
        """Obtiene un usuario por ID"""
        usuario = self.repo.find_by_id(id_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError(f"Usuario {id_usuario} no encontrado")
        return usuario
    
    def obtener_por_email(self, email: str) -> Usuario:
        """Obtiene un usuario por email"""
        usuario = self.repo.find_by_email(email)
        if not usuario:
            raise UsuarioNoEncontradoError(f"Usuario con email {email} no encontrado")
        return usuario
    
    def obtener_por_rol(self, rol: str) -> List[Usuario]:
        """Obtiene usuarios por rol"""
        return self.repo.find_by_rol(rol)
    
    def listar_todos(self) -> List[Usuario]:
        """Lista todos los usuarios"""
        return self.repo.find_all()
    
    def desactivar_usuario(self, id_usuario: int) -> Usuario:
        """Desactiva un usuario (soft delete)"""
        return self.actualizar_usuario(id_usuario, activo=False)
    
    def activar_usuario(self, id_usuario: int) -> Usuario:
        """Activa un usuario"""
        return self.actualizar_usuario(id_usuario, activo=True)
    
    def autenticar(self, email: str, contraseña: str) -> Usuario:
        """
        Autentica un usuario
        
        Reglas de negocio:
        - El usuario debe existir
        - El usuario debe estar activo
        - La contraseña debe ser correcta
        """
        usuario = self.repo.find_by_email(email)
        
        if not usuario:
            raise CredencialesInvalidasError("Email o contraseña incorrectos")
        
        if not usuario.activo:
            raise CredencialesInvalidasError("Usuario inactivo")
        
        if not self._verificar_contraseña(contraseña, usuario.contraseña):
            raise CredencialesInvalidasError("Email o contraseña incorrectos")
        
        return usuario
    
    def cambiar_contraseña(
        self,
        id_usuario: int,
        contraseña_actual: str,
        contraseña_nueva: str
    ) -> Usuario:
        """Cambia la contraseña de un usuario"""
        usuario = self.obtener_por_id(id_usuario)
        
        # Verificar contraseña actual
        if not self._verificar_contraseña(contraseña_actual, usuario.contraseña):
            raise CredencialesInvalidasError("Contraseña actual incorrecta")
        
        # Validar nueva contraseña
        UsuarioValidator.validar_contraseña(contraseña_nueva)
        
        # Actualizar
        return self.actualizar_usuario(id_usuario, contraseña=contraseña_nueva)
    
    @staticmethod
    def _hashear_contraseña(contraseña: str) -> str:
        """Hashea una contraseña con bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(contraseña.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def _verificar_contraseña(contraseña: str, hash_almacenado: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return bcrypt.checkpw(
            contraseña.encode('utf-8'),
            hash_almacenado.encode('utf-8')
        )
