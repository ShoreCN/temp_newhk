from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from enum import Enum

class TaskType(str, Enum):
    RSS = "rss"
    CRAWLER = "crawler"
    MANUAL = "manual"
    OTHER = "other"

class TaskStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class TaskProcessStatus(str, Enum):
    INIT = "init"
    RUNNING = "running"
    FAILED = "failed"
    SUCCESS = "success"

class ContentTask(BaseModel):
    id: Optional[str] = Field(default=None)
    task_type: TaskType
    # name: str = Field(description="任务名称")
    source_url: Optional[str] = Field(description="数据来源地址")
    source_name: str = Field(description="来源名称")
    source_logo: Optional[str] = Field(description="来源logo地址")
    category: str = Field(description="内容所属领域")
    topic: str = Field(description="内容主题")
    update_interval: int = Field(default=86400, description="更新间隔，单位为秒")
    is_hot: bool = Field(default=False, description="是否为热门内容")
    status: TaskStatus = Field(default=TaskStatus.INACTIVE)
    process_status: TaskProcessStatus = Field(default=TaskProcessStatus.INIT)
    last_run_at: Optional[int] = None
    next_run_at: Optional[int] = Field(
        default_factory=lambda: int((datetime.now() + timedelta(seconds=86400)).timestamp())
    )
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp())) 