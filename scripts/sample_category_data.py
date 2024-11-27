import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.category import CategoryType, Category
import asyncio

sample_data_category = [
    {
        "name": "daily",
        "category_type": CategoryType.INFORMATION,
        "description": "日常"
    },
    {
        "name": "food",
        "category_type": CategoryType.INFORMATION,
        "description": "美食"
    },
    {
        "name": "job",
        "category_type": CategoryType.INFORMATION,
        "description": "求职"
    },
    {
        "name": "event",
        "category_type": CategoryType.INFORMATION,
        "description": "活动"
    },
    {
        "name": "shopping",
        "category_type": CategoryType.INFORMATION,
        "description": "购物"
    },
    {
        "name": "news",
        "category_type": CategoryType.INFORMATION,
        "description": "新闻"
    },
    {
        "name": "bank",
        "category_type": CategoryType.GUIDES,
        "description": "银行"
    },
    {
        "name": "communication",
        "category_type": CategoryType.GUIDES,
        "description": "通讯"
    },
    {
        "name": "food",
        "category_type": CategoryType.GUIDES,
        "description": "美食"
    },
    {
        "name": "education",
        "category_type": CategoryType.GUIDES,
        "description": "教育"
    },
    {
        "name": "job",
        "category_type": CategoryType.GUIDES,
        "description": "求职"
    },
    {
        "name": "life",
        "category_type": CategoryType.GUIDES,
        "description": "生活"
    }
]

async def insert_sample_category_data():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    category_list = []
    # 清空现有数据
    r = await db.category.delete_many({})
    print(f"已清空现有分类数据，共删除 {r.deleted_count} 条数据")

    # 将sample_data_category转换为Category对象
    for data in sample_data_category:
        category = Category(**data)
        category_list.append(category.model_dump())
    await db.category.insert_many(category_list)
    print(f"已插入 {len(list(filter(lambda x: x['category_type'] == CategoryType.INFORMATION, category_list)))} 条 {CategoryType.INFORMATION.value} 分类数据")
    print(f"已插入 {len(list(filter(lambda x: x['category_type'] == CategoryType.GUIDES, category_list)))} 条 {CategoryType.GUIDES.value} 分类数据")

if __name__ == "__main__":
    asyncio.run(insert_sample_category_data()) 