from datetime import datetime
from typing import List, Optional
from app.models.task import ContentTask, TaskStatus, TaskType
from app.db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from app.core.rss_config import RSSConfig, RSSFeed

class TaskService:
    def __init__(self):
        self.db = db.db
        self.collection: AsyncIOMotorCollection = self.db.content_tasks
        
    # 如果collection不存在或者为空，则创建并将rss_config中的内容写入
    async def init_collection(self):
        if self.collection is None \
            or self.collection.name not in await self.db.list_collection_names() \
            or await self.collection.count_documents({}) == 0:
            print("content_tasks collection not found, creating...")
            # 创建collection
            # self.collection = await self.db.create_collection("content_tasks")
            # 将rss_config中的内容写入collection
            rss_config = RSSConfig()
            for feed in rss_config.RSS_FEEDS:
                task = self.transfer_feed_to_task(feed)
                await self.collection.insert_one(task.model_dump(exclude={'id'}))
            print("content_tasks collection created and initialized")
        else:
            print("content_tasks collection already exists")
    
    def transfer_feed_to_task(self, feed: RSSFeed) -> ContentTask:
        task = ContentTask(
            task_type=TaskType.RSS,
            source_name=feed.name,
            source_url=feed.relative_path or feed.full_path,
            source_logo=feed.logo,
            category=feed.category,
            topic=feed.topic,
            update_interval=feed.update_interval,
            status=TaskStatus.ACTIVE
        )
        return task

    async def create_task(self, task: ContentTask) -> ContentTask:
        task_dict = task.model_dump(exclude={'id'})
        result = await self.collection.insert_one(task_dict)
        task.id = str(result.inserted_id)
        return task

    async def get_task(self, task_id: str) -> Optional[ContentTask]:
        task = await self.collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task['id'] = str(task.pop('_id'))
            return ContentTask(**task)
        return None

    async def list_tasks(self, skip: int = 0, limit: int = 10) -> List[ContentTask]:
        cursor = self.collection.find().skip(skip).limit(limit)
        tasks = []
        async for task in cursor:
            task['id'] = str(task.pop('_id'))
            tasks.append(ContentTask(**task))
        return tasks

    async def update_task(self, task_id: str, task_update: dict) -> Optional[ContentTask]:
        task_update['updated_at'] = int(datetime.now().timestamp())
        result = await self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": task_update}
        )
        if result.modified_count:
            return await self.get_task(task_id)
        return None

    async def delete_task(self, task_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    async def get_due_tasks(self) -> List[ContentTask]:
        current_time = int(datetime.now().timestamp())
        cursor = self.collection.find({
            "status": TaskStatus.ACTIVE,
            "next_run_at": {"$lte": current_time}
        })
        tasks = []
        async for task in cursor:
            task['id'] = str(task.pop('_id'))
            tasks.append(ContentTask(**task))
        return tasks

    async def clear_all_tasks(self) -> bool:
        """清空所有任务"""
        result = await self.collection.delete_many({})
        return result.deleted_count > 0

    async def set_task_hot(self, task_id: str, is_hot: bool = True) -> Optional[ContentTask]:
        """设置任务的热门状态"""
        return await self.update_task(task_id, {"is_hot": is_hot}) 