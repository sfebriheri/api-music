"""
Database configuration and utilities for PostgreSQL integration
"""
import os
from typing import Optional, Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """Database configuration class"""

    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/mydb')
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', '5432'))
        self.database = os.getenv('DB_NAME', 'mydb')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', '')

    def get_connection_params(self) -> Dict[str, Any]:
        """Get database connection parameters"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password
        }

class DatabaseManager:
    """Database connection manager"""

    def __init__(self):
        self.config = DatabaseConfig()
        self._connection = None

    def connect(self):
        """Establish database connection"""
        try:
            self._connection = psycopg2.connect(**self.config.get_connection_params())
            return self._connection
        except Exception as e:
            raise Exception(f"Failed to connect to database: {str(e)}")

    def disconnect(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        if not self._connection:
            self.connect()

        try:
            with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            self._connection.rollback()
            raise Exception(f"Query execution failed: {str(e)}")

    def execute_command(self, command: str, params: Optional[tuple] = None) -> int:
        """Execute an INSERT, UPDATE, or DELETE command and return affected rows"""
        if not self._connection:
            self.connect()

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(command, params or ())
                affected_rows = cursor.rowcount
                self._connection.commit()
                return affected_rows
        except Exception as e:
            self._connection.rollback()
            raise Exception(f"Command execution failed: {str(e)}")

    def get_tables(self) -> List[str]:
        """Get list of all tables in the database"""
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """
        results = self.execute_query(query)
        return [row['table_name'] for row in results]

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a specific table"""
        query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            AND table_schema = 'public'
            ORDER BY ordinal_position;
        """
        return self.execute_query(query, (table_name,))

# Global database manager instance
db_manager = DatabaseManager()
