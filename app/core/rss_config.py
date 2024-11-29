from typing import Dict, List
from pydantic_settings import BaseSettings
from app.models.content import ContentType

class RSSFeed(BaseSettings):
    content_type: ContentType
    category: str
    url: str
    name: str
    logo: str
    topic: str

class RSSConfig(BaseSettings):
    RSS_FEEDS: List[RSSFeed] = [
        {
            "content_type": ContentType.INFORMATION,
            "category": "news",
            "url": "https://rsshub.speednet.icu/hk01/latest",
            "name": "HK 01",
            "logo": "https://hk01.com/favicon.ico",
            "topic": "香港01最新新闻"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "news",
            "url": "https://rsshub.speednet.icu/hk01/hot",
            "name": "HK 01",
            "logo": "https://hk01.com/favicon.ico",
            "topic": "香港01热门新闻"
        }
    ]
    RSS_UPDATE_INTERVAL: int = 3600  # 默认每小时更新一次

    class Config:
        env_prefix = ""
        case_sensitive = False

rss_settings = RSSConfig()
