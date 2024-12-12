import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import logging
import json
import random
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.services.rss_service import RSSService
from app.core.rss_config import rss_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 测试阶段使用，可以为拉取到的数据增加一些变化性，例如随机设置is_hot属性
def random_change(content: dict):
    # 在拉取到的数据中，随机地将is_hot设置为True的概率是20%
    content['is_hot'] = random.random() < 0.2 
    return content

async def update_rss_content(rss_path: str = None):
    try:
        # Initialize MongoDB client
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        
        # Initialize RSS service
        rss_service = RSSService()
        
        # Filter RSS feeds if rss_path is provided
        if rss_path:
            rss_service.feeds = [
                feed for feed in rss_service.feeds 
                if (feed.relative_path and rss_path in feed.relative_path) or 
                   (feed.full_path and rss_path in feed.full_path)
            ]
            if not rss_service.feeds:
                logger.warning(f"No RSS feeds found matching path: {rss_path}")
                return
            
        while True:
            try:
                # Fetch all content
                contents = await rss_service.fetch_all_content()

                # 写入本地文件， 验证结果是否正确
                with open('rss_content.json', 'w', encoding='utf-8') as f:
                    json.dump([content.model_dump() for content in contents], f, ensure_ascii=False, indent=2)
                    f.write('\n')
                
                # Update database
                for content in contents:
                    # Convert content to dict
                    content_dict = content.dict(exclude={'id'})

                    # Randomly change is_hot attribute for testing
                    content_dict = random_change(content_dict)

                    # Use original_data_path as unique identifier to avoid duplicates
                    result = await db.information.update_one(
                        {'original_data_path': content.original_data_path},
                        {'$set': content_dict},
                        upsert=True
                    )
                    
                    if result.upserted_id:
                        logger.info(f"Inserted new content: {content.topic}")
                    else:
                        logger.info(f"Updated existing content: {content.topic}")
                    
                logger.info(f"Successfully processed {len(contents)} RSS items")
                
            except Exception as e:
                logger.error(f"Error in RSS update cycle: {str(e)}")

            # 测试阶段， 只更新一次
            break
            
            # Wait for the next update interval
            await asyncio.sleep(rss_settings.RSS_UPDATE_INTERVAL)
                
    except Exception as e:
        logger.error(f"Critical error in RSS service: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update RSS content with optional path filtering')
    parser.add_argument('--rss_path', type=str, help='Filter RSS feeds by matching relative_path or full_path')
    args = parser.parse_args()
    
    asyncio.run(update_rss_content(args.rss_path))
