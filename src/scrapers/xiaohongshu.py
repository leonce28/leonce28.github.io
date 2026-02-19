import logging
from typing import List

from .base import BaseScraper, NewsItem
from .utils import MAX_SUMMARY_LENGTH, RequestHelper

logger = logging.getLogger(__name__)


class XiaoHongShuScraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("潮流趋势", top_n)
        self.api_url = "https://api.lolimi.cn/API/jhrb/?hot=微博"

    def fetch(self) -> List[NewsItem]:
        response = RequestHelper.fetch_with_retry(self.api_url)
        if not response:
            logger.warning(f"[{self.name}] No response from API")
            return []

        try:
            data = response.json()
            news_list: List[NewsItem] = []

            if data.get("success") and data.get("data"):
                for item in data["data"][: self.top_n]:
                    title = item.get("title", "")
                    url = item.get("url", "")
                    if title and url:
                        news_list.append(
                            NewsItem(
                                title=self.clean_text(title),
                                url=url,
                                summary="",
                            )
                        )

            logger.info(f"[{self.name}] Fetched {len(news_list)} items")
            return news_list
        except Exception as e:
            logger.error(f"[{self.name}] Failed to parse API response: {e}")
            return []
