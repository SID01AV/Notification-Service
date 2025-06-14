import json
import sys
import logging
import pika
from app.config import EXCHANGE_NAME


logger = logging.getLogger(__name__)


class MessageProcessor:
    def __init__(self, templates_cache, email_service, max_retries=3):
        """
        Initialize the MessageProcessor.

        :param templates_cache: List of templates used for email generation.
        :param email_service: Instance of EmailService for sending emails.
        :param max_retries: Maximum number of retries before routing to DLQ.
        """
        self.templates_cache = templates_cache
        self.email_service = email_service
        self.max_retries = max_retries

    def process_message(self, ch, method, properties, body):
        """
        Process a RabbitMQ message.

        :param ch: Channel object.
        :param method: Delivery method.
        :param properties: Message properties.
        :param body: Message body.
        """
        try:
            # Decode and parse the message
            message = json.loads(body.decode())
            message = json.loads(message)
            logger.info(f"Received message: {message}")

            # Fetch template details
            template_id = message.get("template_id")
            if not template_id:
                raise ValueError("Template ID is missing in the message.")

            # Filter the templates cache to find the template by template_id
            template = next(
                (tmpl for tmpl in self.templates_cache if tmpl["template_id"] == template_id), None
            )

            if not template:
                raise ValueError(f"No template found for template_id: {template_id}")

            # Replace placeholders in the template body
            subject = template["subject"]
            body = template["body"].format(**message["metadata"])

            # Extract email details
            recipient_email = message["user_email"]

            # Use EmailService to send the email
            self.email_service.send_email(recipient_email, subject, body)

            # Acknowledge message after successful email sending
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("Message processed and email sent successfully.")

        except Exception as e:
            self.handle_failure(ch, method, properties, body, e)

    def handle_failure(self, ch, method, properties, body, exception):
        """
        Handle message processing failure.

        :param ch: Channel object.
        :param method: Delivery method.
        :param properties: Message properties.
        :param body: Message body.
        :param exception: Exception raised during processing.
        """
        a, b, c = sys.exc_info()
        line_no = c.tb_lineno
        logger.error(f"Failed to process message: {exception} at line {line_no}")

        # Retry logic
        headers = properties.headers or {}
        retry_count = headers.get("x-retry-count", 0)

        if retry_count < self.max_retries:
            retry_count += 1
            headers["x-retry-count"] = retry_count

            # Publish to retry queue
            ch.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key="retry_queue",
                body=body,
                properties=pika.BasicProperties(
                    headers=headers,
                    delivery_mode=2  # Persistent message
                ),
            )
            logger.info(f"Message retried. Attempt {retry_count}/{self.max_retries}.")
        else:
            # Publish to Dead Letter Queue
            ch.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key="dead_letter_queue",
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2  # Persistent message
                ),
            )
            logger.error("Message moved to Dead Letter Queue.")

        # Acknowledge the original message to avoid duplicate retries
        ch.basic_ack(delivery_tag=method.delivery_tag)

