from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

RABBITMQ_URL = os.getenv('RABBITMQ_URL')
EMAIL_QUEUE_NAMES = {
    "high": "high_priority_queue",
    "medium": "medium_priority_queue",
    "low": "low_priority_queue",
}
EXCHANGE_NAME = os.getenv('EXCHANGE_NAME')

smtp_server=os.getenv('smtp_server')
smtp_port=os.getenv('smtp_port')
smtp_user=os.getenv('smtp_user')
smtp_password=os.getenv('smtp_password')