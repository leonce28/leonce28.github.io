from typing import List

from .base import BaseScraper, NewsItem


class SspaiScraper(BaseScraper):
    rss_url = "https://sspai.com/feed"

    def __init__(self, top_n: int = 10):
        super().__init__("少数派", top_n)

    def fetch(self) -> List[NewsItem]:
        return self._fetch_via_rss()
