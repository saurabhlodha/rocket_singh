from pydantic import BaseModel
from typing import List, Dict


class Message(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    messages: List[Message]
