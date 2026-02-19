import xml.etree.ElementTree as ET
from typing import List, Dict
from .base import BaseScraper
from .utils import AntiScraper


class InfoQScraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("InfoQ", top_n)
        self.rss_url = "https://www.infoq.cn/feed"

    def fetch(self) -> List[Dict]:
        return self._fetch_via_rss()

    def _fetch_via_rss(self) -> List[Dict]:
        response = AntiScraper.fetch_with_retry(
            self.rss_url,
            extra_headers={"Accept": "application/rss+xml,application/xml,text/xml"},
        )
        if not response:
            return []

        try:
            root = ET.fromstring(response.content)
            news_list = []

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
                        summary = self._clean_html(desc_elem.text)
                        if len(summary) > 200:
                            summary = summary[:200] + "..."

                    if title and url:
                        news_list.append(
                            {
                                "title": self.clean_text(title),
                                "url": url,
                                "summary": summary,
                            }
                        )

            return news_list
        except Exception:
            return []

    def _clean_html(self, text: str) -> str:
        import re

        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
