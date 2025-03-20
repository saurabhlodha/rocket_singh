from pydantic import BaseModel
from typing import List, Dict, Optional, Text, Any
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    conversation_id: Optional[int]
    messages: List[MessageBase]

class ConversationResponse(BaseModel):
    id: int
    started_at: datetime
    status: str
    messages: List[Dict]

class SystemPromptUpdate(BaseModel):
    content: Any
