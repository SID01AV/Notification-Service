class DataProcessingError(Exception):
    """Custom exception for errors related to data processing."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class MessagingError(Exception):
    """Custom exception for errors related to message queuing."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
