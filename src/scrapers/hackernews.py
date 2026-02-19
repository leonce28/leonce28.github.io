import logging
from typing import List

from .base import BaseScraper, NewsItem
from .utils import MAX_SUMMARY_LENGTH, RequestHelper

logger = logging.getLogger(__name__)


class HackerNewsScraper(BaseScraper):
    API_BASE = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, top_n: int = 10):
        super().__init__("Hacker News", top_n)

    def fetch(self) -> List[NewsItem]:
        stories_url = f"{self.API_BASE}/topstories.json"
        response = RequestHelper.fetch_with_retry(stories_url)
        if not response:
            logger.warning("[Hacker News] No response from API")
            return []

        story_ids = response.json()[: self.top_n * 2]
        news_list: List[NewsItem] = []

        for story_id in story_ids:
            if len(news_list) >= self.top_n:
                break

            RequestHelper.random_delay(0.3, 0.8)
            item_url = f"{self.API_BASE}/item/{story_id}.json"
            item_response = RequestHelper.fetch_with_retry(item_url)

            if item_response:
                item = item_response.json()
                if item and item.get("title") and item.get("url"):
                    summary = self.clean_text(item.get("text", ""))
                    if summary and len(summary) > MAX_SUMMARY_LENGTH:
                        summary = summary[:MAX_SUMMARY_LENGTH] + "..."
                    news_list.append(
                        NewsItem(
                            title=self.clean_text(item.get("title", "")),
                            url=item.get("url", ""),
                            summary=summary,
                            score=item.get("score", 0),
                            comments=f"https://news.ycombinator.com/item?id={story_id}",
                            descendants=item.get("descendants", 0),
                        )
                    )

        logger.info(f"[Hacker News] Fetched {len(news_list)} items")
        return news_list
