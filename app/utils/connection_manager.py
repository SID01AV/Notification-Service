import pika

class RabbitMQConnectionManager:
    def __init__(self, host: str):
        self.host = host

    def create_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        return connection

    def create_channel(self, connection):
        return connection.channel()
