from .connection_manager import RabbitMQConnectionManager
# from app.config import QUEUE_NAMES

class Consumer:
    def __init__(self, host: str, exchange: str):
        self.connection_manager = RabbitMQConnectionManager(host)
        self.exchange = exchange

    def consume(self, callback, queues:dict):
        connection = self.connection_manager.create_connection()
        channel = self.connection_manager.create_channel(connection)
        channel.exchange_declare(exchange=self.exchange, exchange_type='direct', durable=True)

        for priority in queues.keys():
            queue = queues[priority]
            channel.queue_declare(queue=queue, durable=True)
            channel.queue_bind(exchange=self.exchange, queue=queue, routing_key=queue)
            # Start consuming messages
            channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)
            print(f"Consuming messages from queue: {queue}")
        channel.start_consuming()

# import aio_pika

# class Consumer:
#     def __init__(self, rabbitmq_url: str, exchange: str):
#         self.rabbitmq_url = rabbitmq_url
#         self.exchange = exchange

#     async def consume(self, callback, queues: dict):
#         # Create an asynchronous connection to RabbitMQ
#         connection = await aio_pika.connect_robust(self.rabbitmq_url)
        
#         # Create a channel (robust connection)
#         channel = await connection.channel()

#         # Declare the exchange
#         exchange = await channel.declare_exchange(self.exchange, aio_pika.ExchangeType.DIRECT, durable=True)

#         for priority, queue_name in queues.items():
#             # Declare the queue
#             queue = await channel.declare_queue(queue_name, durable=True)
            
#             # Bind the queue to the exchange with the routing key
#             await queue.bind(exchange, routing_key=queue_name)

#             # Define the callback to handle message consumption
#             async def wrapped_callback(ch, method, properties, body):
#                 # Call the provided callback function
#                 await callback(ch, method, properties, body)

#             # Start consuming messages from the queue using the channel object
#             await queue.consume(wrapped_callback)
#             print(f"Consuming messages from queue: {queue_name}")

#         # We don't need start_consuming() because consume is non-blocking in aio-pika



# import aio_pika

# class RabbitMQConnectionManager:
#     def __init__(self, rabbitmq_url: str):
#         self.rabbitmq_url = rabbitmq_url
#         self.connection = None

#     async def create_connection(self):
#         # Asynchronously connect to RabbitMQ using the full URL
#         self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
#         return self.connection

#     async def create_channel(self, connection):
#         # Asynchronously create a channel
#         return await connection.channel()

#     async def close_connection(self):
#         # Close the connection asynchronously
#         if self.connection:
#             await self.connection.close()


