"""MongoDB connection management."""
import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """Singleton class for managing MongoDB connection."""
    
    _instance: Optional['DatabaseConnection'] = None
    _client: Optional[MongoClient] = None
    _database: Optional[Database] = None
    
    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection."""
        if self._client is None:
            self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB."""
        try:
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            database_name = os.getenv('MONGODB_DATABASE', 'finance_manager')
            
            self._client = MongoClient(mongodb_uri)
            self._database = self._client[database_name]
            
            # Test connection
            self._client.server_info()
            print(f"✓ Connected to MongoDB: {database_name}")
            
            # Create indexes
            self._create_indexes()
            
        except Exception as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        """Create indexes for better query performance."""
        try:
            # Goals collection indexes
            self._database.goals.create_index("user_id")
            self._database.goals.create_index("goal_type")
            self._database.goals.create_index([("user_id", 1), ("created_at", -1)])
            
            # Expenses collection indexes
            self._database.expenses.create_index("user_id")
            self._database.expenses.create_index("category")
            self._database.expenses.create_index([("user_id", 1), ("date", -1)])
            self._database.expenses.create_index([("user_id", 1), ("category", 1)])
            
            # Account balance indexes
            self._database.account_balance.create_index("user_id", unique=True)
            
            print("✓ Database indexes created")
            
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")
    
    @property
    def database(self) -> Database:
        """Get database instance."""
        if self._database is None:
            self._connect()
        return self._database
    
    def close(self):
        """Close database connection."""
        if self._client:
            self._client.close()
            print("✓ MongoDB connection closed")


# Global database instance
db_connection = DatabaseConnection()


def get_database() -> Database:
    """Get database instance for use in tools."""
    return db_connection.database

