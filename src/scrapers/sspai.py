from typing import List, Dict
from bs4 import BeautifulSoup
from .base import BaseScraper
from .utils import AntiScraper


class SspaiScraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("少数派", top_n)
        self.url = "https://sspai.com"

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

        articles = (
            soup.select("a.article-card")
            or soup.select(".item-article a")
            or soup.select("a[href*='/post/']")
        )

        for article in articles[: self.top_n * 2]:
            if len(news_list) >= self.top_n:
                break

            title_elem = article.select_one(".title") or article.select_one("h2")
            title = self.clean_text(title_elem.get_text()) if title_elem else ""

            href = article.get("href", "")
            if title and href:
                if href.startswith("/"):
                    href = f"https://sspai.com{href}"
                news_list.append({"title": title, "url": href})

        if not news_list:
            news_list = self._parse_api()

        return news_list

    def _parse_api(self) -> List[Dict]:
        api_url = "https://sspai.com/api/v1/article/index/page/get?limit=20"
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
            items = data.get("data", []) or []

            for item in items[: self.top_n]:
                slug = item.get("slug", "") or item.get("id", "")
                news_list.append(
                    {
                        "title": self.clean_text(item.get("title", "")),
                        "url": f"https://sspai.com/post/{slug}",
                    }
                )
            return news_list
        except Exception:
            return []
