from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class ContentType(str, Enum):
    INFORMATION = "information"
    GUIDES = "guides"

# class ContentCategory(BaseModel):
#     name: str
#     description: Optional[str] = None

class ListItem(BaseModel):
    name: str
    link: Optional[str] = None
    metrics: Optional[dict] = None
    remarks: Optional[str] = None

class Source(BaseModel):
    name: str
    link: str
    logo: Optional[str] = None

class DataTableItem(BaseModel):
    name: str
    metrics: Optional[dict] = None
    remarks: Optional[str] = None

class DataTable(BaseModel):
    name: str
    details: List[DataTableItem] = None

class GuideContent(BaseModel):
    description: str
    instructions: Optional[str] = None  # 操作指南, 后续可考虑用DSL来实现
    data_table: List[DataTableItem] = None # 目前版本每个指南的数据详情只有一张表 TODO: 后续支持多张表

class Content(BaseModel):
    id: Optional[str] = Field(default=None)
    content_type: ContentType
    category: str
    topic: str
    sub_topic: Optional[str] = None
    tags: Optional[List[str]] = None
    source_list: Optional[List[Source]] = None
    content: Union[List[ListItem], GuideContent, None]
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    is_hot: bool = Field(default=False, description="是否为热门内容")
    next_update_at: Optional[int] = Field(
        default_factory=lambda: int((datetime.now() + timedelta(days=1)).timestamp())
    )

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
    cursor = db.guides.find(
        {"is_hot": True},
        {'_id': 0}
    ).sort("created_at", -1)
    return await cursor.to_list(length=4)
 