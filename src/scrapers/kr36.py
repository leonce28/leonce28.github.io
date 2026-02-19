from typing import List

from .base import BaseScraper, NewsItem


class Kr36Scraper(BaseScraper):
    rss_url = "https://36kr.com/feed"

    def __init__(self, top_n: int = 10):
        super().__init__("36氪", top_n)

    def fetch(self) -> List[NewsItem]:
        return self._fetch_via_rss()
