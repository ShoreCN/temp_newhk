from typing import Dict, List
from enum import Enum
from pydantic_settings import BaseSettings
from app.models.content import ContentType

class FetchMode(str, Enum):
    PRIORITY = "priority"
    RANDOM = "random"

class RSSBaseUrl(BaseSettings):
    url: str
    priority: int = 1
    enabled: bool = True

class RSSFeed(BaseSettings):
    content_type: ContentType
    category: str
    relative_path: str
    name: str
    logo: str
    topic: str

class RSSConfig(BaseSettings):
    FETCH_MODE: FetchMode = FetchMode.PRIORITY
    BASE_URL_POOL: List[RSSBaseUrl] = [
        {
            "url": "https://rsshub.ktachibana.party",
            "priority": 1,
            "enabled": True
        },
        {
            "url": "https://rsshub.speednet.icu",
            "priority": 2,
            "enabled": True
        },
    ]
    
    RSS_FEEDS: List[RSSFeed] = [
        ############################################
        #               新闻类(news)RSS             #
        ############################################
        # HK01系列
        {
            "content_type": ContentType.INFORMATION,
            "category": "news",
            "relative_path": "/hk01/latest",
            "name": "HK 01",
            "logo": "https://hk01.com/favicon.ico",
            "topic": "香港01最新新闻"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "news",
            "relative_path": "/hk01/hot",
            "name": "HK 01",
            "logo": "https://hk01.com/favicon.ico",
            "topic": "香港01热门新闻"
        },
        # 香港经济日报系列
        {
            "content_type": ContentType.INFORMATION,
            "category": "news",
            "relative_path": "/hket/sran001",
            "name": "香港经济日报",
            "logo": "https://www.hket.com/favicon.ico",
            "topic": "香港经济日报: 香港"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "news",
            "relative_path": "/i-cable/news",
            "name": "有线新闻",
            "logo": "https://www.i-cable.com/wp-content/themes/cascara/assets/images/new_logo.svg",
            "topic": "有线宽频: 新闻资讯"
        },

        ############################################
        #               美食类(food)RSS             #
        ############################################
        # OpenRice系列
        {
            "content_type": ContentType.INFORMATION,
            "category": "food",
            "relative_path": "/openrice/zh/hongkong/explore/chart/most-bookmarked",
            "name": "OpenRice",
            "logo": "https://www.openrice.com/favicon.ico",
            "topic": "香港最多收藏餐廳排行榜"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "food",
            "relative_path": "/openrice/zh/hongkong/offers",
            "name": "OpenRice",
            "logo": "https://www.openrice.com/favicon.ico",
            "topic": "香港餐厅精选优惠"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "food",
            "relative_path": "/openrice/zh/hongkong/explore/chart/best-rating",
            "name": "OpenRice",
            "logo": "https://www.openrice.com/favicon.ico",
            "topic": "香港每周最高评分餐厅排行榜"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "food",
            "relative_path": "/openrice/zh/hongkong/promos",
            "name": "OpenRice",
            "logo": "https://www.openrice.com/favicon.ico",
            "topic": "香港餐厅热门活动"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "food",
            "relative_path": "/esquirehk/tag/Food%20&%20Drinks",
            "name": "EsquireHK",
            "logo": "https://www.esquirehk.com/favicon/favicon.ico",
            "topic": "EsquireHK美食推荐"
        },

        ############################################
        #               求职类(job)RSS              #
        ############################################
        {
            "content_type": ContentType.INFORMATION,
            "category": "job",
            "relative_path": "/linkedin/jobs/all/all/%20/geoId=103291313&f_TPR=r86400",
            "name": "Linkedin",
            "logo": "https://www.linkedin.com/favicon.ico",
            "topic": "领英香港最新职位"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "job",
            "relative_path": "/v2ex/tab/jobs",
            "name": "V2EX",
            "logo": "https://v2ex.com/favicon.ico",
            "topic": "V2EX工作板块最新话题"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "job",
            "relative_path": "/eleduck/posts/5",
            "name": "电鸭社区",
            "logo": "https://static.eleduck.com/_next/static/media/icon-500.d77f6cfc.png",
            "topic": "电鸭社区招聘&找人栏目最新话题"
        },

        ############################################
        #               购物类(shopping)RSS         #
        ############################################
        {
            "content_type": ContentType.INFORMATION,
            "category": "shopping",
            "relative_path": "/eprice/hk",
            "name": "ePrice.HK",
            "logo": "https://eprice.hk/favicon.ico",
            "topic": "ePrice最新消息"
        },
        {
            "content_type": ContentType.INFORMATION,
            "category": "shopping",
            "relative_path": "/esquirehk/tag/Fashion",
            "name": "EsquireHK",
            "logo": "https://www.esquirehk.com/favicon/favicon.ico",
            "topic": "EsquireHK潮流资讯"
        },

        ############################################
        #               活动类(event)RSS            #
        ############################################
        {
            "content_type": ContentType.INFORMATION,
            "category": "event",
            "relative_path": "/esquirehk/tag/travel",
            "name": "EsquireHK",
            "logo": "https://www.esquirehk.com/favicon/favicon.ico",
            "topic": "EsquireHK游玩资讯"
        },

        ############################################
        #               生活类(life)RSS             #
        ############################################
        
    ]
    RSS_UPDATE_INTERVAL: int = 3600  # 默认每小时更新一次

    class Config:
        env_prefix = ""
        case_sensitive = False

rss_settings = RSSConfig()
