import feedparser
from typing import List, Optional
from datetime import datetime
import logging
from app.models.content import Content, ContentType, Source, ListItem
from app.core.rss_config import rss_settings, RSSFeed

logger = logging.getLogger(__name__)

class RSSService:
    def __init__(self):
        self.feeds = rss_settings.RSS_FEEDS
    
    def parse_feed(self, feed_url: str) -> Optional[feedparser.FeedParserDict]:
        """Parse RSS feed from given URL"""
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo:  # Check if there was any error during parsing
                logger.error(f"Error parsing feed {feed_url}: {feed.bozo_exception}")
                return None
            return feed
        except Exception as e:
            logger.error(f"Failed to parse feed {feed_url}: {str(e)}")
            return None

    def convert_to_content(self, feed_data: feedparser.FeedParserDict, feed: RSSFeed) -> Content:
        """Convert RSS feed data to Content model"""
        print(feed_data.keys())
        if not feed_data:
            logger.warning(f"Failed to parse feed: {feed.url}")
            return None

        if not feed_data.get("entries"):
            logger.warning(f"No entries found in feed: {feed.url}")
            return None
    
        try:
            source = Source(
                name=feed.name,
                link=feed.url,
                logo=feed.logo
            )
    
            content = Content(
                content_type=feed.content_type,
                category=feed.category,
                topic=feed.topic,
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
                        description=entry.get("description", ""),
                        pub_date=pub_date,
                        source_list=[source]
                    ))
                
                except Exception as e:
                    logger.warning(f"Failed to process entry {entry.get('title', 'unknown')}: {str(e)}")
                    continue
    
            if not content.data:
                logger.warning(f"No valid entries found in feed: {feed.url}")
                return None
    
            return content
    
        except Exception as e:
            logger.error(f"Failed to convert feed to content: {str(e)}")
            return None

    async def fetch_content(self, feed: RSSFeed) -> Content:
        """Fetch and parse feed for a given source"""
        contents = []
        feed_data = self.parse_feed(feed.url)
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
        return all_contents
