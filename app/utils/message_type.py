from abc import ABC, abstractmethod
from app.config import EMAIL_QUEUE_NAMES, EXCHANGE_NAME

class MessageType:
    @abstractmethod
    def get_exchange_name(self):
        pass

    @abstractmethod
    def get_queues(self):
        pass

class EmailMessage(MessageType):
    def get_exchange_name(self):
        return EXCHANGE_NAME
    
    def get_queues(self):
        return EMAIL_QUEUE_NAMES