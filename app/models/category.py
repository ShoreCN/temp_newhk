from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class CategoryType(str, Enum):
    INFORMATION = "information"
    GUIDE = "guide"

class Category(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    category_type: CategoryType = Field(..., description="分类类型")
    parent_id: Optional[str] = Field(None, description="父分类ID")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 

async def get_categories():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    cursor = db.category.find(
        {"category_type": "information"},
        {'_id': 0}
    )
    return await cursor.to_list(length=None) 