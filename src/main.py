import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.jekyll_generator import JekyllGenerator
from src.scrapers import (
    HackerNewsScraper,
    InfoQScraper,
    Kr36Scraper,
    SspaiScraper,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 50)
    logger.info("科技新闻日报生成器")
    logger.info("=" * 50)

    scrapers = [
        HackerNewsScraper(top_n=10),
        Kr36Scraper(top_n=10),
        InfoQScraper(top_n=10),
        SspaiScraper(top_n=10),
    ]

    all_news = {}

    for scraper in scrapers:
        logger.info(f"[{scraper.name}] 正在抓取...")
        try:
            news = scraper.get_news()
            all_news[scraper.name] = news
            logger.info(f"[{scraper.name}] 成功获取 {len(news)} 条新闻")
        except Exception as e:
            logger.error(f"[{scraper.name}] 抓取失败: {e}")
            all_news[scraper.name] = []

    logger.info("=" * 50)

    base_path = Path(__file__).parent.parent
    posts_dir = base_path / "_posts"
    posts_dir.mkdir(parents=True, exist_ok=True)

    jekyll_generator = JekyllGenerator()
    jekyll_content = jekyll_generator.generate_news_post(all_news)
    jekyll_path = base_path / jekyll_generator.get_filename()
    with open(jekyll_path, "w", encoding="utf-8") as f:
        f.write(jekyll_content)
    logger.info(f"[JEKYLL] 新闻已生成: {jekyll_path}")

    logger.info("=" * 50)


if __name__ == "__main__":
    main()
