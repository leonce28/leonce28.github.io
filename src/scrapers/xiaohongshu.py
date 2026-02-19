import logging
from typing import List

from .base import BaseScraper, NewsItem
from .utils import MAX_SUMMARY_LENGTH, RequestHelper

logger = logging.getLogger(__name__)


class XiaoHongShuScraper(BaseScraper):
    rss_url = "https://rsshub.app/xiaohongshu/user/593032945e87e77791e03696/notes"

    def __init__(self, top_n: int = 10):
        super().__init__("小红书", top_n)

    def fetch(self) -> List[NewsItem]:
        return self._fetch_via_rss()
