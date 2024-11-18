import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mongodb_connection():
    try:
        # 替换为您的MongoDB连接URL
        client = AsyncIOMotorClient("mongodb://root:mongopwd@localhost:27017")
        
        # 测试连接
        await client.admin.command('ping')
        logger.info("MongoDB连接成功！")
        
        # 列出所有数据库
        database_list = await client.list_database_names()
        logger.info(f"可用的数据库: {database_list}")
        
        # 关闭连接
        client.close()
        logger.info("MongoDB连接已关闭")
        
    except Exception as e:
        logger.error(f"MongoDB连接测试失败: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection()) 