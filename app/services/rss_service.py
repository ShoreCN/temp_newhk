import feedparser
from typing import List, Optional
from datetime import datetime
import logging
import random
import asyncio
from app.models.content import Content, ContentType, Source, ListItem
from app.core.rss_config import rss_settings, RSSFeed, FetchMode, RSSBaseUrl

logger = logging.getLogger(__name__)

class RSSService:
    def __init__(self):
        self.feeds = rss_settings.RSS_FEEDS
        self.base_urls = rss_settings.BASE_URL_POOL
        self.fetch_mode = rss_settings.FETCH_MODE
    
    def get_base_url(self) -> str:
        """Get base URL based on fetch mode"""
        enabled_urls = [url for url in self.base_urls if url.enabled]
        if not enabled_urls:
            raise ValueError("No enabled base URLs found")
            
        if self.fetch_mode == FetchMode.PRIORITY:
            # Sort by priority (lower number = higher priority)
            sorted_urls = sorted(enabled_urls, key=lambda x: x.priority)
            return sorted_urls[0].url
        else:  # Random mode
            return random.choice(enabled_urls).url
    
    def get_full_url(self, feed: RSSFeed) -> str:
        """Combine base URL with relative path"""
        # If feed has a custom URL, use it
        if feed.full_path:
            return feed.full_path
        
        # Otherwise, combine base URL and relative path
        base_url = self.get_base_url()
        return f"{base_url.rstrip('/')}/{feed.relative_path.lstrip('/')}"

    def parse_feed(self, feed: RSSFeed) -> Optional[feedparser.FeedParserDict]:
        """Parse RSS feed"""
        try:
            full_url = self.get_full_url(feed)
            feed_data = feedparser.parse(full_url)
            if feed_data.bozo:  # Check if there was any error during parsing
                logger.error(f"Error parsing feed {full_url}: {feed_data.bozo_exception}")
                return None
            logger.info(f"Successfully parsed feed {feed.topic} from URL: {full_url}")
            return feed_data
        except Exception as e:
            logger.error(f"Failed to parse feed {feed.relative_path}: {str(e)}")
            return None

    def convert_to_content(self, feed_data: feedparser.FeedParserDict, feed: RSSFeed) -> Content:
        """Convert RSS feed data to Content model"""
        # print(feed_data.keys())
        # import json
        # with open('rss_feed_data.json', 'w', encoding='utf-8') as f:
        #     json.dump(feed_data, f, ensure_ascii=False, indent=2)

        if not feed_data:
            logger.warning(f"Failed to parse feed: {feed.relative_path}")
            return None

        if not feed_data.get("entries"):
            logger.warning(f"No entries found in feed: {feed.relative_path}")
            return None
    
        try:
            source = Source(
                name=feed.name,
                link=feed_data.get("feed", {}).get("link", ""),
                logo=feed.logo,
                rss_path=feed.full_path if feed.full_path else feed.relative_path
            )
    
            content = Content(
                content_type=feed.content_type,
                category=feed.category,
                topic=feed.topic,
                sub_topic=feed_data.get("feed", {}).get("title", ""),  # 使用数据源的标题作为子主题
                original_data_path=feed.full_path if feed.full_path else feed.relative_path,
                source_list=[source],
                data=[]  # Initialize the data list
            )
    
            for entry in feed_data["entries"]:
                try:
                    # Validate required fields
                    if not all(key in entry for key in ["title", "link"]):
                        logger.warning(f"Missing required fields in entry: {entry}")
                        continue
    
                    # Handle pub_date parsing with multiple formats
                    pub_date = None
                    if "published" in entry:
                        try:
                            # Try ISO format first
                            pub_date = datetime.fromisoformat(entry["published"])
                        except ValueError:
                            try:
                                # Try parsing with feedparser's date handler
                                pub_date = datetime(*entry.published_parsed[:6])
                            except (TypeError, ValueError):
                                logger.warning(f"Could not parse publication date: {entry.get('published')}")
                                pub_date = datetime.now()
    
                    content.data.append(ListItem(
                        name=entry["title"],
                        link=entry["link"],
                        metrics={
                            # "description": entry.get("description", ""),
                            "pub_date": int(pub_date.timestamp()) if pub_date else None,
                        }
                    ))
                
                except Exception as e:
                    logger.warning(f"Failed to process entry {entry.get('title', 'unknown')}: {str(e)}")
                    continue
    
            if not content.data:
                logger.warning(f"No valid entries found in feed: {feed.relative_path}")
                return None
    
            return content
    
        except Exception as e:
            logger.error(f"Failed to convert feed to content: {str(e)}")
            return None

    async def fetch_content(self, feed: RSSFeed) -> Content:
        """Fetch and parse feed for a given source"""
        contents = []
        feed_data = self.parse_feed(feed)
        if feed_data:
            content = self.convert_to_content(feed_data, feed)
            if content:
                contents.append(content)
            
        return contents
        

    async def fetch_all_content(self) -> List[Content]:
        """Fetch and parse all configured feeds"""
        all_contents = []
        for feed in self.feeds:
            contents = await self.fetch_content(feed)
            all_contents.extend(contents)

            # 打印任务完成信息
            logger.info(f"Finished fetching content for {feed.topic}")

            # 测试时, 可以放开这一行，拉取一条进行验证
            # break
            
            # 拉取完每条任务后等待5秒
            await asyncio.sleep(5)
        return all_contents
