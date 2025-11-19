import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    database_url: Optional[str] = os.getenv('DATABASE_URL')
    host: str = os.getenv('DB_HOST', 'localhost')
    port: str = os.getenv('DB_PORT', '5432')
    database: str = os.getenv('DB_NAME', 'postgres')
    user: str = os.getenv('DB_USER', 'postgres')
    password: str = os.getenv('DB_PASSWORD', 'postgres')

class PostgresRepository:
    """Manages PostgreSQL database connections and operations"""
    
    def __init__(self):
        self.config = DatabaseConfig()
        
    def get_connection(self):
        """Create and return a database connection"""
        if self.config.database_url:
            return psycopg2.connect(self.config.database_url)
        
        return psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password
        )

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            raise Exception(f"Database query failed: {str(e)}")
        finally:
            if conn:
                conn.close()

    def execute_command(self, command: str, params: Optional[Tuple] = None) -> int:
        """Execute INSERT, UPDATE, DELETE commands and return affected rows"""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute(command, params)
                affected_rows = cur.rowcount
                conn.commit()
                return affected_rows
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Database command failed: {str(e)}")
        finally:
            if conn:
                conn.close()

    def get_tables(self) -> List[str]:
        """List all tables in the public schema"""
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """
        results = self.execute_query(query)
        return [row['table_name'] for row in results]

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a specific table"""
        query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """
        return self.execute_query(query, (table_name,))
