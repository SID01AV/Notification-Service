from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import uuid
from fastapi import HTTPException
from app.utils.db_utils import Database, Message
import logging

logger = logging.getLogger(__name__)

class MessageDBHandler:
    def __init__(self, database: Database):
        self.database = database

    async def save_message(self, client_id: int, message_data: dict) -> str:
        """Save a message to the database."""
        async for session in self.database.get_session():  # Use `async with` to handle session
        # async with self.database.get_session() as session:
            try:
                message = Message(
                    id=str(uuid.uuid4()),
                    client_id=client_id,
                    template_id=message_data["template_id"],
                    message_format=message_data["message_format"],
                    user_email=message_data["user_email"],
                    priority=message_data["priority"],
                    message_data=message_data["metadata"],
                    status="PENDING",
                )
                session.add(message)  # Use the session to add the object
                await session.commit()  # Commit transaction
                return message.id
            except SQLAlchemyError as e:
                await session.rollback()  # Rollback the transaction if an error occurs
                logger.error(f"Error saving message: {e}")
                raise HTTPException(status_code=500, detail="Failed to save message to the database.")

    async def update_status(self, message_id: str, status: str):
        """Update the status of a message."""
        async for session in self.database.get_session():  # Use `async with` to handle session
            try:
                query = select(Message).where(Message.id == message_id)
                result = await session.execute(query)  # Use session.execute() with the async session
                message = result.scalars().first()  # Extract the first result

                if not message:
                    raise HTTPException(status_code=404, detail=f"Message with ID {message_id} not found.")

                message.status = status
                await session.commit()  # Commit the updated status
            except SQLAlchemyError as e:
                await session.rollback()  # Rollback the transaction if an error occurs
                raise HTTPException(status_code=500, detail="Failed to update message status.")
