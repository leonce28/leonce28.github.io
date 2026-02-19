import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scrapers import HackerNewsScraper, Kr36Scraper, InfoQScraper, SspaiScraper
from src.generator import MarkdownGenerator
from src.html_generator import HtmlGenerator
from src.jekyll_generator import JekyllGenerator


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

    base_path = Path(__file__).parent.parent
    news_dir = base_path / "news"
    news_dir.mkdir(parents=True, exist_ok=True)

    _news_dir = base_path / "_news"
    _news_dir.mkdir(parents=True, exist_ok=True)

    md_generator = MarkdownGenerator()
    md_content = md_generator.generate(all_news)
    md_path = base_path / md_generator.get_filename()
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[MD] 文件已生成: {md_path}")

    html_generator = HtmlGenerator()
    html_content = html_generator.generate(all_news)
    html_path = base_path / html_generator.get_filename()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[HTML] 文件已生成: {html_path}")

    index_content = html_generator.generate_index(news_dir)
    index_path = news_dir / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"[INDEX] 索引已更新: {index_path}")

    jekyll_generator = JekyllGenerator()
    jekyll_content = jekyll_generator.generate_news_post(all_news)
    jekyll_path = base_path / jekyll_generator.get_filename()
    with open(jekyll_path, "w", encoding="utf-8") as f:
        f.write(jekyll_content)
    print(f"[JEKYLL] 新闻已生成: {jekyll_path}")

    print("=" * 50)


if __name__ == "__main__":
    main()
