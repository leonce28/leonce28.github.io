from abc import ABC, abstractmethod
from typing import List, Dict
from .utils import AntiScraper


class BaseScraper(ABC):
    def __init__(self, name: str, top_n: int = 10):
        self.name = name
        self.top_n = top_n

    @abstractmethod
    def fetch(self) -> List[Dict]:
        pass

    def get_news(self) -> List[Dict]:
        try:
            news = self.fetch()
            return news[: self.top_n]
        except Exception as e:
            print(f"[{self.name}] Error fetching news: {e}")
            return []

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        return " ".join(text.split()).strip()
