import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scrapers import HackerNewsScraper, Kr36Scraper, InfoQScraper, SspaiScraper
from src.generator import MarkdownGenerator


def main():
    print("=" * 50)
    print("科技新闻日报生成器")
    print("=" * 50)

    scrapers = [
        HackerNewsScraper(top_n=10),
        Kr36Scraper(top_n=10),
        InfoQScraper(top_n=10),
        SspaiScraper(top_n=10),
    ]

    all_news = {}

    for scraper in scrapers:
        print(f"\n[{scraper.name}] 正在抓取...")
        try:
            news = scraper.get_news()
            all_news[scraper.name] = news
            print(f"[{scraper.name}] 成功获取 {len(news)} 条新闻")
        except Exception as e:
            print(f"[{scraper.name}] 抓取失败: {e}")
            all_news[scraper.name] = []

    print("\n" + "=" * 50)
    print("正在生成 Markdown 文件...")

    generator = MarkdownGenerator()
    content = generator.generate(all_news)
    filename = generator.get_filename()

    output_path = Path(__file__).parent.parent / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"文件已生成: {output_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
