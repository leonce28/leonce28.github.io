import json
import logging
import re
from typing import List
from bs4 import BeautifulSoup

from .base import BaseScraper, NewsItem
from .utils import MAX_SUMMARY_LENGTH, RequestHelper

logger = logging.getLogger(__name__)


class XiaoHongShuScraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("小红书", top_n)
        self.url = "https://www.xiaohongshu.com/explore"

    def fetch(self) -> List[NewsItem]:
        response = RequestHelper.fetch_with_retry(self.url)
        if not response:
            logger.warning(f"[{self.name}] No response from {self.url}")
            return []

        try:
            soup = BeautifulSoup(response.content, "lxml")
            news_list: List[NewsItem] = []

            scripts = soup.find_all("script")
            for script in scripts:
                if script.string and "window.__INITIAL_STATE__" in script.string:
                    data = self._parse_initial_state(script.string)
                    if data:
                        news_list = self._extract_from_json_data(data)
                        break

            if not news_list:
                news_list = self._fallback_parse(soup)

            logger.info(f"[{self.name}] Fetched {len(news_list)} items")
            return news_list[: self.top_n]
        except Exception as e:
            logger.error(f"[{self.name}] Failed to parse page: {e}")
            return []

    def _parse_initial_state(self, script_content: str) -> dict | None:
        try:
            match = re.search(
                r"window\.__INITIAL_STATE__\s*=\s*({.*?});",
                script_content,
                re.DOTALL,
            )
            if match:
                return json.loads(match.group(1))
        except Exception as e:
            logger.debug(f"Failed to parse initial state: {e}")
        return None

    def _extract_from_json_data(self, data: dict) -> List[NewsItem]:
        news_list: List[NewsItem] = []
        try:
            if "note" in data:
                notes = data["note"]
                for note_id, note_data in notes.items():
                    if isinstance(note_data, dict):
                        title = note_data.get("title", "")
                        url = f"https://www.xiaohongshu.com/explore/{note_id}"
                        if title:
                            news_list.append(
                                NewsItem(
                                    title=self.clean_text(title),
                                    url=url,
                                    summary="",
                                )
                            )
        except Exception as e:
            logger.debug(f"Failed to extract from JSON: {e}")
        return news_list

    def _fallback_parse(self, soup: BeautifulSoup) -> List[NewsItem]:
        news_list: List[NewsItem] = []

        items = soup.find_all("a", href=re.compile(r"/explore/[a-zA-Z0-9]+"))
        seen_urls = set()
        for item in items:
            href = item.get("href", "")
            if href in seen_urls:
                continue
            seen_urls.add(href)

            title = ""
            title_elem = item.find("span") or item.find("p") or item
            if title_elem:
                title = title_elem.get_text(strip=True)

            if not title:
                img = item.find("img")
                if img and img.get("alt"):
                    title = img.get("alt", "")[:100]

            if title and href:
                url = (
                    "https://www.xiaohongshu.com" + href
                    if not href.startswith("http")
                    else href
                )
                news_list.append(
                    NewsItem(
                        title=self.clean_text(title),
                        url=url,
                        summary="",
                    )
                )

        return news_list
