import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import logging
import json
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.services.rss_service import RSSService
from app.core.rss_config import rss_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def update_rss_content():
    try:
        # Initialize MongoDB client
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        
        # Initialize RSS service
        rss_service = RSSService()
        
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
    asyncio.run(update_rss_content())
