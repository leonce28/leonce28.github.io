from typing import List, Dict
from bs4 import BeautifulSoup
from .base import BaseScraper
from .utils import AntiScraper


class Kr36Scraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("36氪", top_n)
        self.url = "https://36kr.com"

    def fetch(self) -> List[Dict]:
        response = AntiScraper.fetch_with_retry(
            self.url,
            extra_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        if not response:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        news_list = []

        articles = soup.select("a.article-item-title") or soup.select(
            ".hot-list-item a"
        )

        for article in articles[: self.top_n * 2]:
            if len(news_list) >= self.top_n:
                break

            title = self.clean_text(article.get_text())
            href = article.get("href", "")

            if title and href:
                if href.startswith("/"):
                    href = f"https://36kr.com{href}"
                news_list.append({"title": title, "url": href})

        if not news_list:
            news_list = self._parse_api()

        return news_list

    def _parse_api(self) -> List[Dict]:
        api_url = "https://gateway.36kr.com/api/mis/nav/home/navList"
        response = AntiScraper.fetch_with_retry(
            api_url,
            extra_headers={
                "Accept": "application/json",
            },
        )
        if not response:
            return []

        try:
            data = response.json()
            news_list = []
            items = data.get("data", {}).get("list", []) or []

            for item in items[: self.top_n]:
                news_list.append(
                    {
                        "title": self.clean_text(item.get("title", "")),
                        "url": f"https://36kr.com/p/{item.get('id', '')}",
                    }
                )
            return news_list
        except Exception:
            return []
