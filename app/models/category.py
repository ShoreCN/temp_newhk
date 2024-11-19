from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

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