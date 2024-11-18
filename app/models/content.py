from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

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

async def get_hot_information():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    cursor = db.information.find(
        {"is_hot": True},
        {'_id': 0}
    ).sort("created_at", -1)
    return await cursor.to_list(length=5)

async def get_hot_guides():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    cursor = db.guide.find(
        {"is_hot": True},
        {'_id': 0}
    ).sort("created_at", -1)
    return await cursor.to_list(length=4)
 