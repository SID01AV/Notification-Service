import sys
import os
import json
import asyncio

# Add the parent directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import DATABASE_URL, smtp_password, smtp_port, smtp_server, smtp_user
from app.utils.db_utils import Database
from app.utils.template_service import TemplateService
from worker.message_processor import MessageProcessor
import logging

from app.utils.consumer import Consumer
from app.utils.message_type import EmailMessage
from app.utils.email_utils import EmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize the email service (use your SMTP details)
email_service = EmailService(
    smtp_server=smtp_server,
    smtp_port=smtp_port,
    smtp_user=smtp_user,
    smtp_password=smtp_password
)

async def fetch_all_templates(db):
    template_service = TemplateService(db)
    all_templates = await template_service.get_all_templates()
    return all_templates

# def process_message(ch, method, properties, body, templates_cache):
#     try:
#         # Decode and parse the message
#         message = json.loads(body.decode())
#         message = json.loads(message)
#         logger.info(f"Received message: {message}")

#         # Fetch template details using `template_id`
#         template_id = message.get('template_id')
#         if not template_id:
#             raise ValueError("Template ID is missing in the message.")

#         # Filter the templates cache to find the template by template_id
#         template = next((tmpl for tmpl in templates_cache if tmpl['template_id'] == template_id), None)

#         if not template:
#             raise ValueError(f"No template found for template_id: {template_id}")

#         # Replace placeholders in the template body
#         subject = template['subject']
#         body = template['body'].format(**message['metadata'])

#         # Extract email details
#         recipient_email = message['user_email']

#         # Send the email
#         email_service.send_email(recipient_email=recipient_email, subject=subject, body=body)

#         # Acknowledge message after successful email sending
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#         logger.info("Message processed and email sent successfully.")

#     except Exception as e:
#         a, b, c = sys.exc_info()
#         line_no = c.tb_lineno
#         logger.error(f"Failed to process message or send email: {e} - {line_no}")
#         # NACK the message to avoid losing it
#         ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)



async def main():
    try:
        logger.info("Starting the consumer...")

        # Initialize the database and fetch all templates at startup
        db = Database(DATABASE_URL)
        templates_cache = await fetch_all_templates(db)

        message_type = EmailMessage()
        exchange = message_type.get_exchange_name()
        queues = message_type.get_queues()

        processor = MessageProcessor(templates_cache=templates_cache, email_service=email_service)

        # Here, we need an event loop to handle async processing
        consumer = Consumer(host='localhost', exchange=exchange)

        # Use asyncio to start the consumer and handle async functions in the message processing
        consumer.consume(callback=lambda ch, method, properties, body: processor.process_message(ch, method, properties, body), queues=queues)
    except KeyboardInterrupt:
        logger.info("Consumer stopped manually.")

# Run the main function in the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
