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

            note_cards = soup.find_all("div", class_=re.compile(r"note-card"))

            if not note_cards:
                notes = soup.find_all("div", {"data-module": re.compile(r"note|mix")})
                for note in notes[: self.top_n * 2]:
                    if len(news_list) >= self.top_n:
                        break
                    item = self._parse_note(note)
                    if item:
                        news_list.append(item)
            else:
                for card in note_cards[: self.top_n * 2]:
                    if len(news_list) >= self.top_n:
                        break
                    item = self._parse_note_card(card)
                    if item:
                        news_list.append(item)

            logger.info(f"[{self.name}] Fetched {len(news_list)} items")
            return news_list
        except Exception as e:
            logger.error(f"[{self.name}] Failed to parse page: {e}")
            return []

    def _parse_note_card(self, card) -> NewsItem | None:
        try:
            title_elem = card.find("h3") or card.find("a", class_=re.compile(r"title"))
            title = ""
            if title_elem:
                title = title_elem.get_text(strip=True)

            if not title:
                img_elem = card.find("img")
                if img_elem and img_elem.get("alt"):
                    title = img_elem.get("alt", "")[:100]

            link_elem = card.find("a", href=re.compile(r"/explore/"))
            url = ""
            if link_elem:
                href = link_elem.get("href", "")
                if href:
                    url = (
                        "https://www.xiaohongshu.com" + href
                        if not href.startswith("http")
                        else href
                    )

            if not title or not url:
                return None

            like_elem = card.find(string=re.compile(r"\d+"))
            summary = ""
            if like_elem:
                summary = f"点赞: {like_elem.strip()}"

            return NewsItem(
                title=self.clean_text(title),
                url=url,
                summary=summary,
            )
        except Exception as e:
            logger.debug(f"Failed to parse note card: {e}")
            return None

    def _parse_note(self, note) -> NewsItem | None:
        try:
            title = ""
            url = ""

            link = note.find("a", href=re.compile(r"/explore/"))
            if link:
                href = link.get("href", "")
                url = (
                    "https://www.xiaohongshu.com" + href
                    if not href.startswith("http")
                    else href
                )
                title_elem = link.find("span") or link.find("p") or link
                if title_elem:
                    title = title_elem.get_text(strip=True)

            img = note.find("img")
            if not title and img and img.get("alt"):
                title = img.get("alt", "")[:100]

            if not title or not url:
                return None

            return NewsItem(
                title=self.clean_text(title),
                url=url,
                summary="",
            )
        except Exception as e:
            logger.debug(f"Failed to parse note: {e}")
            return None
