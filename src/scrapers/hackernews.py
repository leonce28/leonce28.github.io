from typing import List, Dict
from .base import BaseScraper
from .utils import AntiScraper


class HackerNewsScraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("Hacker News", top_n)
        self.api_base = "https://hacker-news.firebaseio.com/v0"

    def fetch(self) -> List[Dict]:
        stories_url = f"{self.api_base}/topstories.json"
        response = AntiScraper.fetch_with_retry(stories_url)
        if not response:
            return []

        story_ids = response.json()[: self.top_n * 2]
        news_list = []

        for story_id in story_ids:
            if len(news_list) >= self.top_n:
                break

            AntiScraper.random_delay(0.3, 0.8)
            item_url = f"{self.api_base}/item/{story_id}.json"
            item_response = AntiScraper.fetch_with_retry(item_url)

            if item_response:
                item = item_response.json()
                if item and item.get("title") and item.get("url"):
                    news_list.append(
                        {
                            "title": self.clean_text(item.get("title", "")),
                            "url": item.get("url", ""),
                            "score": item.get("score", 0),
                            "comments": f"https://news.ycombinator.com/item?id={story_id}",
                            "descendants": item.get("descendants", 0),
                        }
                    )

        return news_list
