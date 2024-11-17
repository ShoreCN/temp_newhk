import aioredis
from app.core.config import settings
import json

class RedisCache:
    def __init__(self):
        self.redis = None
        
    async def connect(self):
        self.redis = await aioredis.from_url(settings.REDIS_URL)
        
    async def get(self, key: str):
        if not self.redis:
            await self.connect()
        value = await self.redis.get(key)
        return json.loads(value) if value else None
        
    async def set(self, key: str, value: any):
        if not self.redis:
            await self.connect()
        await self.redis.set(
            key,
            json.dumps(value),
            ex=settings.REDIS_CACHE_EXPIRE
        )

cache = RedisCache() 