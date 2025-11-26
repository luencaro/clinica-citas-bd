"""
Repositorio de Usuario
"""

from typing import List, Optional
from database import db
from models.usuario import Usuario
from .base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """Repositorio para operaciones con usuarios"""
    
    def __init__(self):
        super().__init__('usuario', Usuario)
    
    def create(
        self,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        contraseña: str,
        rol: str,
        activo: bool = True
    ) -> Usuario:
        """Crea un nuevo usuario"""
        query = """
            INSERT INTO usuario (nombre, apellido, email, telefono, contraseña, rol, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_usuario, nombre, apellido, email, telefono, contraseña, rol, fecha_creacion, activo
        """
        result = db.execute_query(
            query,
            (nombre, apellido, email, telefono, contraseña, rol, activo),
            fetch='one'
        )
        return Usuario.from_db_row(result)
    
    def update(
        self,
        id_usuario: int,
        nombre: str = None,
        apellido: str = None,
        email: str = None,
        telefono: str = None,
        contraseña: str = None,
        rol: str = None,
        activo: bool = None
    ) -> Optional[Usuario]:
        """Actualiza un usuario"""
        updates = []
        params = []
        
        if nombre is not None:
            updates.append("nombre = %s")
            params.append(nombre)
        if apellido is not None:
            updates.append("apellido = %s")
            params.append(apellido)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if telefono is not None:
            updates.append("telefono = %s")
            params.append(telefono)
        if contraseña is not None:
            updates.append("contraseña = %s")
            params.append(contraseña)
        if rol is not None:
            updates.append("rol = %s")
            params.append(rol)
        if activo is not None:
            updates.append("activo = %s")
            params.append(activo)
        
        if not updates:
            return self.find_by_id(id_usuario)
        
        params.append(id_usuario)
        query = f"""
            UPDATE usuario 
            SET {', '.join(updates)}
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre, apellido, email, telefono, contraseña, rol, fecha_creacion, activo
        """
        
        result = db.execute_query(query, tuple(params), fetch='one')
        return Usuario.from_db_row(result) if result else None
    
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca usuario por email"""
        query = "SELECT * FROM usuario WHERE email = %s"
        result = db.execute_query(query, (email,), fetch='one')
        return Usuario.from_db_row(result) if result else None
    
    def find_by_telefono(self, telefono: str) -> Optional[Usuario]:
        """Busca usuario por teléfono"""
        query = "SELECT * FROM usuario WHERE telefono = %s"
        result = db.execute_query(query, (telefono,), fetch='one')
        return Usuario.from_db_row(result) if result else None
    
    def find_by_rol(self, rol: str) -> List[Usuario]:
        """Busca usuarios por rol"""
        query = "SELECT * FROM usuario WHERE rol = %s AND activo = TRUE"
        results = db.execute_query(query, (rol,), fetch='all')
        return [Usuario.from_db_row(row) for row in results]
    
    def exists_email(self, email: str, exclude_id: int = None) -> bool:
        """Verifica si existe un email (excluyendo opcionalmente un ID)"""
        if exclude_id:
            query = "SELECT 1 FROM usuario WHERE email = %s AND id_usuario != %s LIMIT 1"
            result = db.execute_query(query, (email, exclude_id), fetch='one')
        else:
            query = "SELECT 1 FROM usuario WHERE email = %s LIMIT 1"
            result = db.execute_query(query, (email,), fetch='one')
        return result is not None
    
    def exists_telefono(self, telefono: str, exclude_id: int = None) -> bool:
        """Verifica si existe un teléfono (excluyendo opcionalmente un ID)"""
        if exclude_id:
            query = "SELECT 1 FROM usuario WHERE telefono = %s AND id_usuario != %s LIMIT 1"
            result = db.execute_query(query, (telefono, exclude_id), fetch='one')
        else:
            query = "SELECT 1 FROM usuario WHERE telefono = %s LIMIT 1"
            result = db.execute_query(query, (telefono,), fetch='one')
        return result is not None
