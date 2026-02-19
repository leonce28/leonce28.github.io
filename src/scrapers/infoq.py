from typing import List

from .base import BaseScraper, NewsItem


class InfoQScraper(BaseScraper):
    rss_url = "https://infoq.com/feed"

    def __init__(self, top_n: int = 10):
        super().__init__("InfoQ", top_n)

    def fetch(self) -> List[NewsItem]:
        return self._fetch_via_rss()
