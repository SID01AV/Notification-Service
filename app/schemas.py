from pydantic import BaseModel, Field, RootModel
from typing import List, Dict, Any


class NotificationRequest(BaseModel):
    client_id: str
    priority: str
    notifications: List[Dict]

Metadata = RootModel[Dict[str, Any]]

class DataItem(BaseModel):
    template_id: int
    user_email: str
    metadata: Metadata
    priority: str = Field(..., pattern="^(high|medium|low)$")  # Priority column

    class Config:
        # This is to handle any extra fields in the metadata dynamically.
        extra = "allow"

    def to_dict(self):
        return self.dict()

class InputData(BaseModel):
    client_id: int
    message_format: str
    data: List[DataItem]


# Custom serialization function
def custom_serializer(obj):
    if isinstance(obj, DataItem):
        return obj.to_dict()  # Convert DataItem to dictionary
    if isinstance(obj, dict):  # This is for metadata which is a dictionary
        return obj  # Just return the dictionary as is
    raise TypeError(f"Type {type(obj)} not serializable")