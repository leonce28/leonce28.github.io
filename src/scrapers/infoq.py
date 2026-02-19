from typing import List, Dict
from bs4 import BeautifulSoup
from .base import BaseScraper
from .utils import AntiScraper


class InfoQScraper(BaseScraper):
    def __init__(self, top_n: int = 10):
        super().__init__("InfoQ", top_n)
        self.url = "https://www.infoq.cn"

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
            soup.select("a.article-item")
            or soup.select(".list-item a")
            or soup.select("a[href*='/article/']")
        )

        for article in articles[: self.top_n * 2]:
            if len(news_list) >= self.top_n:
                break

            title_elem = article.select_one(".article-title") or article.select_one(
                "h3"
            )
            title = self.clean_text(title_elem.get_text()) if title_elem else ""

            href = article.get("href", "")
            if title and href:
                if href.startswith("/"):
                    href = f"https://www.infoq.cn{href}"
                news_list.append({"title": title, "url": href})

        if not news_list:
            news_list = self._parse_api()

        return news_list

    def _parse_api(self) -> List[Dict]:
        api_url = "https://www.infoq.cn/public/v1/article/getList"
        response = AntiScraper.fetch_with_retry(
            api_url,
            extra_headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        if not response:
            return []

        try:
            data = response.json()
            news_list = []
            items = data.get("data", []) or []

            for item in items[: self.top_n]:
                uuid = item.get("uuid", "")
                news_list.append(
                    {
                        "title": self.clean_text(item.get("article_title", "")),
                        "url": f"https://www.infoq.cn/article/{uuid}",
                    }
                )
            return news_list
        except Exception:
            return []
