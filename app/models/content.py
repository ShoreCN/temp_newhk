from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

T = TypeVar('T')

class ContentType(str, Enum):
    INFORMATION = "information"
    GUIDES = "guides"

class SearchContentType(str, Enum):
    INFORMATION = "information"
    GUIDES = "guides"
    ALL = "all"

class SearchSuggestionType(str, Enum):
    TOPIC = "topic"
    TITLE = "title"
    TAG = "tag"
    CATEGORY = "category"
    SOURCE = "source"

class SearchSuggestion(BaseModel, Generic[T]):
    suggestion_type: SearchSuggestionType
    content_type: Optional[ContentType]
    name: str
    id: Optional[str] = Field(default=None)
    data: Optional[T] = None

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
    rss_path: Optional[str] = None

class DataTableItem(BaseModel):
    name: str
    metrics: Optional[dict] = None
    remarks: Optional[str] = None

class DataTable(BaseModel):
    name: str
    details: List[DataTableItem] = None

class GuideData(BaseModel):
    description: str
    instructions: Optional[str] = None  # 操作指南, 后续可考虑用DSL来实现
    data_table: List[DataTableItem] = None # 目前版本每个指南的数据详情只有一张表 TODO: 后续支持多张表

class Content(BaseModel):
    id: Optional[str] = Field(default=None)
    content_type: ContentType
    category: str = Field(description="对应产品设计里的领域")
    topic: str = Field(description="主题")
    title: Optional[str] = Field(description="对外展示的标题")
    sub_title: Optional[str] = None
    original_data_path: Optional[str] = None # 原始数据采集源的地址, 对外不可见, 作为内部MongoDB的唯一标识
    tags: Optional[List[str]] = None
    source_list: Optional[List[Source]] = None
    data: Union[List[ListItem], GuideData, None]
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    is_hot: bool = Field(default=False, description="是否为热门内容")
    update_interval: Optional[int] = Field(default=86400, description="更新间隔，单位为秒") # 默认每天更新一次
    next_update_at: Optional[int] = Field(
        default_factory=lambda: int((datetime.now() + timedelta(seconds=86400)).timestamp())
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
 