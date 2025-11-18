"""
Database Configuration Module
============================================================================
Manages database connection parameters and configuration settings
"""

import os
from typing import Dict


class DatabaseConfig:
    """Database configuration class"""
    
    def __init__(self):
        """Initialize database configuration from environment variables"""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 5432))
        self.database = os.getenv('DB_NAME', 'clinica_citas')
        self.user = os.getenv('DB_USER', 'clinica_admin')
        self.password = os.getenv('DB_PASSWORD', 'clinica_2025_secure')
        
        # Connection pool settings
        self.min_connections = int(os.getenv('DB_MIN_CONN', 1))
        self.max_connections = int(os.getenv('DB_MAX_CONN', 10))
        
        # Connection retry settings
        self.max_retries = int(os.getenv('DB_MAX_RETRIES', 5))
        self.retry_delay = int(os.getenv('DB_RETRY_DELAY', 5))
        
    def get_connection_string(self) -> str:
        """
        Get database connection string
        
        Returns:
            str: PostgreSQL connection string
        """
        return (
            f"host={self.host} "
            f"port={self.port} "
            f"dbname={self.database} "
            f"user={self.user} "
            f"password={self.password}"
        )
    
    def get_connection_dict(self) -> Dict[str, any]:
        """
        Get database connection parameters as dictionary
        
        Returns:
            Dict: Connection parameters
        """
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password
        }
    
    def __repr__(self) -> str:
        """String representation (hiding password)"""
        return (
            f"DatabaseConfig(host='{self.host}', "
            f"port={self.port}, "
            f"database='{self.database}', "
            f"user='{self.user}')"
        )


class AppConfig:
    """Application configuration class"""
    
    def __init__(self):
        """Initialize application configuration"""
        self.environment = os.getenv('APP_ENV', 'development')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.debug = self.environment == 'development'
        
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == 'development'


# Global configuration instances
db_config = DatabaseConfig()
app_config = AppConfig()
