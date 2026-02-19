import html
import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import List, Optional, TypedDict

from .utils import MAX_SUMMARY_LENGTH, RequestHelper

logger = logging.getLogger(__name__)


class NewsItem(TypedDict, total=False):
    title: str
    url: str
    summary: str
    score: Optional[int]
    comments: Optional[str]
    descendants: Optional[int]


class BaseScraper(ABC):
    rss_url: Optional[str] = None

    def __init__(self, name: str, top_n: int = 10):
        self.name = name
        self.top_n = top_n

    @abstractmethod
    def fetch(self) -> List[NewsItem]:
        pass

    def get_news(self) -> List[NewsItem]:
        try:
            news = self.fetch()
            return news[: self.top_n]
        except Exception as e:
            logger.error(f"[{self.name}] Error fetching news: {e}")
            return []

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        return " ".join(text.split()).strip()

    @staticmethod
    def escape_html(text: str) -> str:
        return html.escape(text)

    def _fetch_via_rss(self) -> List[NewsItem]:
        if not self.rss_url:
            logger.error(f"[{self.name}] RSS URL not configured")
            return []

        response = RequestHelper.fetch_with_retry(
            self.rss_url,
            extra_headers={"Accept": "application/rss+xml,application/xml,text/xml"},
        )
        if not response:
            logger.warning(f"[{self.name}] No response from RSS feed")
            return []

        try:
            root = ET.fromstring(response.content)
            news_list: List[NewsItem] = []

            for item in root.findall(".//item")[: self.top_n * 2]:
                if len(news_list) >= self.top_n:
                    break

                title_elem = item.find("title")
                link_elem = item.find("link")
                desc_elem = item.find("description")

                if title_elem is not None and link_elem is not None:
                    title = title_elem.text or ""
                    url = link_elem.text or ""
                    summary = ""
                    if desc_elem is not None and desc_elem.text:
                        summary = RequestHelper.clean_html(desc_elem.text)
                        if len(summary) > MAX_SUMMARY_LENGTH:
                            summary = summary[:MAX_SUMMARY_LENGTH] + "..."

                    if title and url:
                        news_list.append(
                            NewsItem(
                                title=self.clean_text(title),
                                url=url,
                                summary=summary,
                            )
                        )

            logger.info(f"[{self.name}] Fetched {len(news_list)} items from RSS")
            return news_list
        except ET.ParseError as e:
            logger.error(f"[{self.name}] Failed to parse RSS XML: {e}")
            return []
