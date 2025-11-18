"""
Database Connection Module
============================================================================
Handles database connection with retry logic and connection pooling
"""

import time
import logging
import psycopg2
from psycopg2 import pool, OperationalError, DatabaseError
from typing import Optional, Tuple
from contextlib import contextmanager

from config import db_config

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Database connection manager with connection pooling and retry logic
    """
    
    def __init__(self):
        """Initialize database connection manager"""
        self.config = db_config
        self.connection_pool: Optional[pool.SimpleConnectionPool] = None
        self._is_connected = False
        
    def connect_with_retry(self) -> bool:
        """
        Establish database connection with retry logic
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        logger.info("Attempting to connect to database...")
        logger.info(f"Configuration: {self.config}")
        
        for attempt in range(1, self.config.max_retries + 1):
            try:
                logger.info(f"Connection attempt {attempt}/{self.config.max_retries}")
                
                # Try to create connection pool
                self.connection_pool = pool.SimpleConnectionPool(
                    self.config.min_connections,
                    self.config.max_connections,
                    **self.config.get_connection_dict()
                )
                
                # Test connection
                conn = self.connection_pool.getconn()
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                db_version = cursor.fetchone()
                cursor.close()
                self.connection_pool.putconn(conn)
                
                self._is_connected = True
                logger.info("✓ Database connection established successfully!")
                logger.info(f"PostgreSQL version: {db_version[0]}")
                return True
                
            except OperationalError as e:
                logger.warning(f"Connection attempt {attempt} failed: {str(e)}")
                
                if attempt < self.config.max_retries:
                    logger.info(f"Retrying in {self.config.retry_delay} seconds...")
                    time.sleep(self.config.retry_delay)
                else:
                    logger.error("Max retries reached. Could not connect to database.")
                    return False
                    
            except Exception as e:
                logger.error(f"Unexpected error during connection: {str(e)}")
                return False
        
        return False
    
    @contextmanager
    def get_cursor(self, commit: bool = False):
        """
        Context manager for database cursor
        
        Args:
            commit: Whether to commit transaction on success
            
        Yields:
            Cursor object
            
        Example:
            with db.get_cursor(commit=True) as cursor:
                cursor.execute("INSERT INTO...")
        """
        if not self._is_connected or not self.connection_pool:
            raise RuntimeError("Database not connected. Call connect_with_retry() first.")
        
        conn = self.connection_pool.getconn()
        cursor = conn.cursor()
        
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            cursor.close()
            self.connection_pool.putconn(conn)
    
    def execute_query(self, query: str, params: Optional[tuple] = None, 
                     fetch: str = 'all') -> Optional[list]:
        """
        Execute a SELECT query
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch: Fetch mode ('all', 'one', or 'none')
            
        Returns:
            Query results or None
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                
                if fetch == 'all':
                    return cursor.fetchall()
                elif fetch == 'one':
                    return cursor.fetchone()
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        try:
            with self.get_cursor(commit=True) as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
                
        except Exception as e:
            logger.error(f"Update execution failed: {str(e)}")
            raise
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test database connection and return status
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            result = self.execute_query("SELECT CURRENT_DATABASE(), CURRENT_USER;", fetch='one')
            if result:
                return True, f"Connected to database '{result[0]}' as user '{result[1]}'"
            return False, "Query returned no results"
            
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
    
    def get_table_count(self, table_name: str) -> int:
        """
        Get row count for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of rows in the table
        """
        try:
            query = f"SELECT COUNT(*) FROM {table_name};"
            result = self.execute_query(query, fetch='one')
            return result[0] if result else 0
            
        except Exception as e:
            logger.error(f"Failed to get count for table {table_name}: {str(e)}")
            return 0
    
    def get_all_tables(self) -> list:
        """
        Get list of all tables in the database
        
        Returns:
            List of table names
        """
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """
        try:
            results = self.execute_query(query)
            return [row[0] for row in results] if results else []
            
        except Exception as e:
            logger.error(f"Failed to get table list: {str(e)}")
            return []
    
    def close(self):
        """Close all database connections"""
        if self.connection_pool:
            self.connection_pool.closeall()
            self._is_connected = False
            logger.info("Database connections closed")
    
    @property
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self._is_connected


# Global database connection instance
db = DatabaseConnection()
