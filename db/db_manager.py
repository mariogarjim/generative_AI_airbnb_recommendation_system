from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class DatabaseManager:
    """Class to manage database initialization and sessions."""
    
    def __init__(self, database_uri="sqlite:///airbnb.db"):
        """
        Initialize the DatabaseManager with a database URI.
        Creates the engine and session factory.
        """
        self.database_uri = database_uri
        self.engine = create_engine(self.database_uri)
        self.Session = sessionmaker(bind=self.engine)
    
    def init_db(self):
        """
        Initialize the database by creating all tables.
        Ensures the database schema matches the models defined in `Base`.
        """
        Base.metadata.create_all(self.engine)
        print("Tables created successfully.")
    
    def get_session(self):
        """
        Provide a session for database operations.
        Returns:
            session: A SQLAlchemy session object.
        """
        return self.Session()
