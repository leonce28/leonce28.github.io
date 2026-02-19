from datetime import datetime
from typing import Dict, List


class MarkdownGenerator:
    def __init__(self):
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y-%m-%d")
        self.date_display = self.date.strftime("%Y年%m月%d日")

    def generate(self, all_news: Dict[str, List[Dict]]) -> str:
        sections = []

        sections.append(f"# 科技新闻日报 - {self.date_display}")
        sections.append("")

        for source_name, news_list in all_news.items():
            if not news_list:
                continue

            sections.append(f"## {source_name} Top {len(news_list)}")
            sections.append("")

            for idx, news in enumerate(news_list, 1):
                title = news.get("title", "无标题")
                url = news.get("url", "")
                score = news.get("score")
                descendants = news.get("descendants")
                comments = news.get("comments")

                if score is not None:
                    sections.append(f"{idx}. [{title}]({url})")
                    sections.append(
                        f"   - {score} points | [{descendants or 0} comments]({comments})"
                    )
                    sections.append("")
                else:
                    sections.append(f"{idx}. [{title}]({url})")
                    sections.append("")

            sections.append("---")
            sections.append("")

        sections.append(f"*生成时间: {self.date.strftime('%Y-%m-%d %H:%M:%S')} CST*")

        return "\n".join(sections)

    def get_filename(self) -> str:
        return f"news/{self.date_str}.md"
