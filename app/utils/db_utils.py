from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine, TIMESTAMP, JSON, func
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Define the base for models
Base = declarative_base()

# Template model
class Template(Base):
    __tablename__ = 'templates'

    template_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(String, nullable=False)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(Integer, nullable=False)
    message_format = Column(String(20), nullable=False)
    template_id = Column(Integer, nullable=False)
    user_email = Column(String(255), nullable=False)
    priority = Column(String(10), nullable=False)
    message_data = Column(JSON, nullable=False)
    status = Column(String(20), default='pending', nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class Database:
    def __init__(self, database_url: str):
        # Store the database URL
        self.database_url = database_url
        
        # Create the asynchronous engine using asyncpg
        self.engine = create_async_engine(self.database_url, echo=True)
        
        # Create a sessionmaker for async sessions
        self.SessionLocal = sessionmaker(
            bind=self.engine, 
            class_=AsyncSession, 
            autocommit=False, 
            autoflush=False
        )
    
    async def get_session(self):
        """Returns an asynchronous session."""
        async with self.SessionLocal() as session:
            yield session

    async def close_session(self, session):
        """Close the async session."""
        await session.close()