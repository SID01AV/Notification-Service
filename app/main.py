from fastapi import FastAPI, HTTPException
import logging
import asyncio
from app.schemas import InputData
import sys
from app.exceptions import DataProcessingError, MessagingError
# from app.config import QUEUE_NAMES
from app.utils.publisher import Publisher 
from app.utils.message_type import EmailMessage
from app.utils.messagedb_service import MessageDBHandler
from app.utils.db_utils import Database
from app.config import DATABASE_URL

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

db = Database(DATABASE_URL)

app = FastAPI()

@app.get("/")
def home():
    try:
        return ("Hello World")
    except:
        return ('Error hai bhaiya')
   
@app.post("/send-notification")
async def send_notification(input_data: InputData):
    try:
        if input_data.message_format == 'email':
            message_type = EmailMessage()

        message_handler = MessageDBHandler(db)

        publisher = Publisher(host='localhost',exchange=message_type.get_exchange_name())
        tasks = []
        queues = message_type.get_queues()
        for priority in queues.keys():
            messages = [item for item in input_data.data if item.priority == priority]
            # When iterating over messages, convert each DataItem instance to a dictionary
            # for message_data in messages:
            #     # Convert DataItem to dictionary
            #     message_data_dict = message_data.to_dict()
            #     message_data_dict["message_format"] = input_data.message_format
            #     # Save message to DB and get its ID
            #     message_id = await message_handler.save_message(
            #         client_id=input_data.client_id, message_data=message_data_dict
            #     )

            #     # Add the message ID before publishing
            #     message_data_dict["message_id"] = message_id

            if messages:
                tasks.append(publisher.publish(messages, priority, queues))
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)

        return {"message": "Data processed and sent to the queue."}
    except DataProcessingError as e:
        logger.error(f"Data processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Data processing failed: {e.message}")
    
    except MessagingError as e:
        logger.error(f"Message queue error: {e}")
        raise HTTPException(status_code=500, detail=f"Message queue error: {e.message}")
    
    except Exception as e:
        a, b, c = sys.exc_info()
        line_no = c.tb_lineno
        logger.error(f"Unexpected error: {e}-{line_no}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#template registration