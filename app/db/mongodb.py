from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    async def connect_to_database(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.db = self.client[settings.DATABASE_NAME]
            # 测试连接
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB")
        except Exception as e:
            print(f"Could not connect to MongoDB: {e}")
            raise e
        
    async def close_database_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

db = MongoDB()