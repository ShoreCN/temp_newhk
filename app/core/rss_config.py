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
        },
        # OpenRice系列
        {
            "content_type": ContentType.INFORMATION,
            "category": "food",
            "url": "https://rsshub.ktachibana.party/openrice/zh/hongkong/explore/chart/most-bookmarked",
            "name": "OpenRice",
            "logo": "https://www.openrice.com/favicon.ico",
            "topic": "香港最多收藏餐廳排行榜"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "food",
            "url": "https://rsshub.ktachibana.party/openrice/zh/hongkong/offers",
            "name": "OpenRice",
            "logo": "https://www.openrice.com/favicon.ico",
            "topic": "香港美食优惠活动"
        },
        # 香港经济日报系列
        {
            "content_type": ContentType.INFORMATION,
            "category": "news",
            "url": "https://rsshub.ktachibana.party/hket/sran001",
            "name": "香港经济日报",
            "logo": "https://www.hket.com/favicon.ico",
            "topic": "香港经济日报: 香港"
        }
    ]
    RSS_UPDATE_INTERVAL: int = 3600  # 默认每小时更新一次

    class Config:
        env_prefix = ""
        case_sensitive = False

rss_settings = RSSConfig()
