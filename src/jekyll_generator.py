from datetime import datetime
from typing import Dict, List
from pathlib import Path


class JekyllGenerator:
    def __init__(self):
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y-%m-%d")

    def generate_news_post(self, all_news: Dict[str, List[Dict]]) -> str:
        sources_yaml = ""
        for source_name, news_list in all_news.items():
            if news_list:
                sources_yaml += (
                    f"  - name: {source_name}\n    count: {len(news_list)}\n"
                )

        front_matter = f"""---
layout: news
title: 科技新闻日报
date: {self.date_str}
categories: [news]
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

        return front_matter + "\n" + "\n".join(content_sections)

    def _escape_html(self, text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def get_filename(self) -> str:
        return f"_news/{self.date_str}.md"
