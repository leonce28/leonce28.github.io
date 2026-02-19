import json
from typing import List, Dict
from .base import BaseScraper
from .utils import AntiScraper


class Kr36Scraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("36氪", top_n)

    def fetch(self) -> List[Dict]:
        return self._fetch_hot_articles()

    def _fetch_hot_articles(self) -> List[Dict]:
        api_url = "https://gateway.36kr.com/api/mis/nav/home/navList/flow"
        payload = {"partner_id": "wap", "param": {"pageEvent": 1, "pageSize": 20}}

        response = AntiScraper.fetch_with_retry(
            api_url,
            extra_headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://36kr.com",
                "Referer": "https://36kr.com/",
            },
        )

        if response:
            try:
                data = response.json()
                items = data.get("data", {}).get(" itemList", []) or data.get(
                    "data", {}
                ).get("itemList", [])
                news_list = []
                for item in items[: self.top_n]:
                    article = item.get("item", item)
                    title = article.get("title", "") or article.get(
                        "templateMaterial", {}
                    ).get("title", "")
                    article_id = article.get("id", "") or article.get("entityId", "")
                    if title and article_id:
                        news_list.append(
                            {
                                "title": self.clean_text(title),
                                "url": f"https://36kr.com/p/{article_id}",
                            }
                        )
                if news_list:
                    return news_list
            except Exception:
                pass

        return self._fetch_via_rss()

    def _fetch_via_rss(self) -> List[Dict]:
        import xml.etree.ElementTree as ET

        rss_url = "https://36kr.com/feed"
        response = AntiScraper.fetch_with_retry(rss_url)
        if not response:
            return []

        try:
            root = ET.fromstring(response.content)
            news_list = []
            for item in root.findall(".//item")[: self.top_n]:
                title_elem = item.find("title")
                link_elem = item.find("link")
                if title_elem is not None and link_elem is not None:
                    news_list.append(
                        {
                            "title": self.clean_text(title_elem.text or ""),
                            "url": link_elem.text or "",
                        }
                    )
            return news_list
        except Exception:
            return []
