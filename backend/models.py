from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    messages: List[Message]

class CustomPrompt(BaseModel):
    content: str
    timestamp: Optional[datetime] = None
