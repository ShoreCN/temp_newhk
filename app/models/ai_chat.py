from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: MessageRole
    content: str
    
class ChatSession(BaseModel):
    session_id: str
    device_id: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    device_id: str
    message: str
    
class ChatResponse(BaseModel):
    session_id: str
    message: str
    sources: List[dict] = [] 