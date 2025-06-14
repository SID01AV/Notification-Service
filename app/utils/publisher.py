from app.utils.connection_manager import RabbitMQConnectionManager
import json
import pika
from app.schemas import custom_serializer

class Publisher:
    def __init__(self, host: str, exchange: str):
        self.connection_manager = RabbitMQConnectionManager(host)
        self.exchange = exchange

    async def publish(self, data_items, priority, queues: dict):
        connection = self.connection_manager.create_connection()
        channel = self.connection_manager.create_channel(connection)

        queue = queues[priority]

        channel.exchange_declare(exchange=self.exchange, exchange_type='direct', durable=True)
        channel.queue_declare(queue=queue, durable=True)

        channel.queue_bind(exchange=self.exchange, queue=queue, routing_key=queue)

        for item in data_items:
            message = json.dumps(item, default=custom_serializer)
            channel.basic_publish(
            exchange=self.exchange,
            routing_key=queue,  # routing key matches the queue name
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )
        
        connection.close()
