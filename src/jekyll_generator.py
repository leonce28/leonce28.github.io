import html
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List
from zoneinfo import ZoneInfo

from .scrapers import NewsItem

logger = logging.getLogger(__name__)

CHINA_TZ = ZoneInfo("Asia/Shanghai")


class JekyllGenerator:
    def __init__(self):
        self.date = datetime.now(CHINA_TZ)
        self.date_str = self.date.strftime("%Y-%m-%d")
        self.datetime_str = self.date.strftime("%Y-%m-%d %H:%M:%S %z")

    def generate_news_post(self, all_news: Dict[str, List[NewsItem]]) -> str:
        sources_yaml = ""
        for source_name, news_list in all_news.items():
            if news_list:
                sources_yaml += (
                    f"  - name: {source_name}\n    count: {len(news_list)}\n"
                )

        front_matter = f"""---
title: "科技新闻日报 {self.date_str}"
date: {self.datetime_str}
categories: [News]
tags: [news, daily-news]
description: "每日自动抓取 Hacker News、36氪、InfoQ、少数派的热门科技新闻。"
author: 撑花儿
pin: true
sources:
{sources_yaml}---
"""

        content_sections = []

        for source_name, news_list in all_news.items():
            if not news_list:
                continue

            section = f"## {source_name} Top {len(news_list)}\n\n"
            section += "<ol>\n"

            for news in news_list:
                title = news.get("title", "无标题")
                url = news.get("url", "#")
                summary = news.get("summary", "")
                score = news.get("score")
                descendants = news.get("descendants", 0)
                comments = news.get("comments", "")

                li_content = f'<li>\n<strong><a href="{url}" target="_blank" rel="noopener">{self._escape_html(title)}</a></strong>'

                if summary:
                    li_content += f"\n<br><small>{self._escape_html(summary)}</small>"

                if score is not None:
                    li_content += f'\n<br><span class="meta">{score} pts'
                    if comments:
                        li_content += f' | <a href="{comments}" target="_blank">{descendants} 评论</a>'
                    li_content += "</span>"

                li_content += "\n</li>"
                section += li_content + "\n"

            section += "</ol>\n"
            content_sections.append(section)

        logger.info(f"Generated news post for {self.date_str}")
        return front_matter + "\n" + "\n".join(content_sections)

    def _escape_html(self, text: str) -> str:
        return html.escape(text)

    def get_filename(self) -> str:
        return f"_posts/{self.date_str}-daily-tech-news.md"
