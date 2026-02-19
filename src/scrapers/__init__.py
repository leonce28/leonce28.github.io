from .base import BaseScraper, NewsItem
from .hackernews import HackerNewsScraper
from .infoq import InfoQScraper
from .kr36 import Kr36Scraper
from .sspai import SspaiScraper

__all__ = [
    "BaseScraper",
    "NewsItem",
    "HackerNewsScraper",
    "Kr36Scraper",
    "InfoQScraper",
    "SspaiScraper",
]
