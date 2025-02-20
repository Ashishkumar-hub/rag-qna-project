from sqlalchemy import Column, Integer, String, LargeBinary, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from app.core.logging_config import logger

# Base class for declarative class definitions
Base = declarative_base()


class Document(Base):
    """
    Represents a document stored in the database.

    Attributes:
        id (int): Primary key for the document.
        text (str): The textual content of the document.
        embedding (bytes): The document's vector embedding stored as binary data.
    """

    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    embedding = Column(LargeBinary)  # Store embeddings as binary


# Database setup
try:
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database: {e}")
