import xml.etree.ElementTree as ET
from typing import List, Dict
from .base import BaseScraper
from .utils import AntiScraper


class SspaiScraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("少数派", top_n)
        self.rss_url = "https://sspai.com/feed"

    def fetch(self) -> List[Dict]:
        return self._fetch_via_rss()

    def _fetch_via_rss(self) -> List[Dict]:
        response = AntiScraper.fetch_with_retry(
            self.rss_url,
            extra_headers={
                "Accept": "application/rss+xml,application/xml,text/xml",
            },
        )
        if not response:
            return self._fetch_via_api()

        try:
            root = ET.fromstring(response.content)
            news_list = []

            for item in root.findall(".//item")[: self.top_n * 2]:
                if len(news_list) >= self.top_n:
                    break

                title_elem = item.find("title")
                link_elem = item.find("link")

                if title_elem is not None and link_elem is not None:
                    title = title_elem.text or ""
                    url = link_elem.text or ""

                    if title and url:
                        news_list.append(
                            {
                                "title": self.clean_text(title),
                                "url": url,
                            }
                        )

            return news_list
        except Exception:
            return self._fetch_via_api()

    def _fetch_via_api(self) -> List[Dict]:
        api_url = "https://sspai.com/api/v1/article/index/page/get?limit=20&offset=0"
        response = AntiScraper.fetch_with_retry(
            api_url,
            extra_headers={
                "Accept": "application/json",
                "Origin": "https://sspai.com",
                "Referer": "https://sspai.com/",
            },
        )

        if not response:
            return []

        try:
            data = response.json()
            news_list = []
            items = data.get("data", []) or data.get("list", [])

            for item in items[: self.top_n]:
                slug = item.get("slug", "") or item.get("id", "")
                title = item.get("title", "")
                if title and slug:
                    news_list.append(
                        {
                            "title": self.clean_text(title),
                            "url": f"https://sspai.com/post/{slug}",
                        }
                    )

            return news_list
        except Exception:
            return []
