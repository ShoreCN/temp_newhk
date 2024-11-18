from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    INFORMATION = "information"
    GUIDE = "guide"

class ContentDomain(BaseModel):
    name: str
    description: Optional[str] = None

class ListItem(BaseModel):
    name: str
    link: Optional[str] = None
    metrics: Optional[dict] = None
    remarks: Optional[str] = None

class GuideContent(BaseModel):
    description: str
    data_table: Optional[dict] = None
    instructions: Optional[str] = None

class Content(BaseModel):
    id: Optional[str] = Field(default=None)
    content_type: ContentType
    domain: ContentDomain
    topic: str
    content: Union[List[ListItem], GuideContent]
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    is_hot: bool = Field(default=False, description="是否为热门内容")
 