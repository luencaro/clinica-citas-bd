"""
Repositorio Base - Implementa operaciones CRUD genéricas
"""

from typing import List, Optional, TypeVar, Generic, Tuple
from database import db

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Repositorio base con operaciones CRUD genéricas
    """
    
    def __init__(self, table_name: str, model_class):
        self.table_name = table_name
        self.model_class = model_class
    
    def find_by_id(self, id_value: int, id_column: str = None) -> Optional[T]:
        """Busca un registro por ID"""
        if id_column is None:
            id_column = f"id_{self.table_name}"
        
        query = f"SELECT * FROM {self.table_name} WHERE {id_column} = %s"
        result = db.execute_query(query, (id_value,), fetch='one')
        
        if result:
            return self.model_class.from_db_row(result)
        return None
    
    def find_all(self, limit: int = None, offset: int = 0, order_by: str = None) -> List[T]:
        """Obtiene todos los registros"""
        query = f"SELECT * FROM {self.table_name}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        results = db.execute_query(query, fetch='all')
        return [self.model_class.from_db_row(row) for row in results]
    
    def count(self) -> int:
        """Cuenta el total de registros"""
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        result = db.execute_query(query, fetch='one')
        return result[0] if result else 0
    
    def delete_by_id(self, id_value: int, id_column: str = None) -> bool:
        """Elimina un registro por ID"""
        if id_column is None:
            id_column = f"id_{self.table_name}"
        
        query = f"DELETE FROM {self.table_name} WHERE {id_column} = %s"
        db.execute_query(query, (id_value,))
        return True
    
    def exists(self, id_value: int, id_column: str = None) -> bool:
        """Verifica si existe un registro"""
        if id_column is None:
            id_column = f"id_{self.table_name}"
        
        query = f"SELECT 1 FROM {self.table_name} WHERE {id_column} = %s LIMIT 1"
        result = db.execute_query(query, (id_value,), fetch='one')
        return result is not None
