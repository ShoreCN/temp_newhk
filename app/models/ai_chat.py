from pydantic import BaseModel, Field, model_serializer
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class SessionStatus(str, Enum):
    ACTIVE = "active"
    STOPPED = "stopped"
    EXPIRED = "expired"

class Source(BaseModel):
    title: str
    url: str

class Message(BaseModel):
    role: MessageRole
    content: str
    sources: List[Source] = []
    created_at: datetime = Field(default_factory=datetime.now)

class SessionInfo(BaseModel):
    name: str = Field(default="")  # 默认和first_message相同, 可以修改
    first_message: str
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    model: str = "deepseek-chat"
    status: SessionStatus = SessionStatus.ACTIVE
    stop_reason: Optional[str] = None
    request_count: int = 0

class ChatSession(BaseModel):
    session_id: str
    device_id: str
    session_info: SessionInfo
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class ChatSessionResponse(ChatSession):
    created_at: int = Field(default=int(datetime.now().timestamp()))
    updated_at: int = Field(default=int(datetime.now().timestamp()))
    
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    device_id: str
    message: str
    
class ChatResponse(BaseModel):
    session_id: str
    content: str
    sources: List[Source] = []
    suggestions: List[str] = []

class MessageResponse(BaseModel):
    role: MessageRole
    content: str
    sources: List[Source] = []
    created_at: int = Field(default=int(datetime.now().timestamp()))

class ChatHistoryResponse(BaseModel):
    session_id: str
    device_id: str
    messages: List[MessageResponse]
    created_at: int = Field(default=int(datetime.now().timestamp()))
    updated_at: int = Field(default=int(datetime.now().timestamp()))
