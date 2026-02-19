import os
from datetime import datetime
from typing import Dict, List
from pathlib import Path


class HtmlGenerator:
    def __init__(self):
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y-%m-%d")
        self.date_display = self.date.strftime("%Y年%m月%d日")

    def generate(self, all_news: Dict[str, List[Dict]]) -> str:
        sections = []
        for source_name, news_list in all_news.items():
            if not news_list:
                continue
            sections.append(self._generate_section(source_name, news_list))

        return self._get_template().format(
            date_display=self.date_display,
            date_str=self.date_str,
            sections="\n".join(sections),
            timestamp=self.date.strftime("%Y-%m-%d %H:%M:%S CST"),
        )

    def _generate_section(self, source_name: str, news_list: List[Dict]) -> str:
        cards = []
        for idx, news in enumerate(news_list, 1):
            cards.append(self._generate_card(idx, news))

        return f"""
        <section class="source-section">
            <h2 class="source-title">{source_name} Top {len(news_list)}</h2>
            <div class="news-grid">
                {"".join(cards)}
            </div>
        </section>"""

    def _generate_card(self, idx: int, news: Dict) -> str:
        title = news.get("title", "无标题")
        url = news.get("url", "#")
        summary = news.get("summary", "")
        score = news.get("score")
        descendants = news.get("descendants", 0)
        comments = news.get("comments", "")

        meta_html = ""
        if score is not None:
            meta_html = f'''
                <div class="news-meta">
                    <span class="score">{score} pts</span>
                    <span class="comments">
                        <a href="{comments}" target="_blank">{descendants} 评论</a>
                    </span>
                </div>'''

        summary_html = ""
        if summary:
            summary_html = f'<p class="news-summary">{self._escape_html(summary)}</p>'

        return f'''
                <article class="news-card">
                    <div class="news-header">
                        <span class="news-rank">{idx}</span>
                        <h3 class="news-title">
                            <a href="{url}" target="_blank" rel="noopener">{self._escape_html(title)}</a>
                        </h3>
                    </div>
                    {summary_html}
                    <div class="news-footer">
                        {meta_html}
                        <a href="{url}" target="_blank" rel="noopener" class="read-more">阅读全文 →</a>
                    </div>
                </article>'''

    def _escape_html(self, text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def _get_template(self) -> str:
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技新闻日报 - {date_display}</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📰</text></svg>">
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent: #58a6ff;
            --accent-hover: #79b8ff;
            --border: #30363d;
            --success: #3fb950;
            --shadow: rgba(0, 0, 0, 0.3);
        }

        [data-theme="light"] {
            --bg-primary: #f6f8fa;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --text-primary: #24292f;
            --text-secondary: #57606a;
            --text-muted: #8c959f;
            --accent: #0969da;
            --accent-hover: #0550ae;
            --border: #d0d7de;
            --shadow: rgba(0, 0, 0, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 3px var(--shadow);
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            font-size: 32px;
        }

        h1 {
            font-size: 24px;
            font-weight: 600;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .theme-toggle {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .theme-toggle:hover {
            background: var(--border);
        }

        .nav-links {
            display: flex;
            gap: 15px;
        }

        .nav-links a {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            padding: 8px 12px;
            border-radius: 6px;
            transition: all 0.2s;
        }

        .nav-links a:hover {
            background: var(--bg-card);
            color: var(--accent);
        }

        main {
            padding: 30px 0;
        }

        .date-info {
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: 30px;
            font-size: 14px;
        }

        .source-section {
            margin-bottom: 40px;
        }

        .source-title {
            font-size: 20px;
            font-weight: 600;
            padding-bottom: 12px;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--accent);
            display: inline-block;
        }

        .news-grid {
            display: grid;
            gap: 16px;
        }

        .news-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.2s;
        }

        .news-card:hover {
            border-color: var(--accent);
            box-shadow: 0 4px 12px var(--shadow);
            transform: translateY(-2px);
        }

        .news-header {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 10px;
        }

        .news-rank {
            background: var(--accent);
            color: white;
            font-size: 12px;
            font-weight: 600;
            width: 24px;
            height: 24px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .news-title {
            font-size: 16px;
            font-weight: 500;
            line-height: 1.4;
        }

        .news-title a {
            color: var(--text-primary);
            text-decoration: none;
        }

        .news-title a:hover {
            color: var(--accent);
        }

        .news-summary {
            color: var(--text-secondary);
            font-size: 14px;
            line-height: 1.6;
            margin: 10px 0 12px 36px;
        }

        .news-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-left: 36px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .news-meta {
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 13px;
            color: var(--text-muted);
        }

        .score {
            color: var(--success);
            font-weight: 500;
        }

        .comments a {
            color: var(--text-muted);
            text-decoration: none;
        }

        .comments a:hover {
            color: var(--accent);
        }

        .read-more {
            color: var(--accent);
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
        }

        .read-more:hover {
            color: var(--accent-hover);
            text-decoration: underline;
        }

        footer {
            text-align: center;
            padding: 30px 0;
            color: var(--text-muted);
            font-size: 13px;
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }

        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }

            h1 {
                font-size: 20px;
            }

            .news-summary {
                margin-left: 0;
            }

            .news-footer {
                margin-left: 0;
            }

            .news-card {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📰</span>
                    <h1>科技新闻日报 - {date_display}</h1>
                </div>
                <div class="header-actions">
                    <nav class="nav-links">
                        <a href="index.html">📁 历史归档</a>
                    </nav>
                    <button class="theme-toggle" onclick="toggleTheme()">
                        <span id="theme-icon">🌙</span>
                        <span id="theme-text">深色</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <main class="container">
        <p class="date-info">每日自动更新 | 北京时间 08:00</p>
        {sections}
    </main>

    <footer>
        <div class="container">
            <p>生成时间: {timestamp}</p>
            <p style="margin-top: 8px;">由 GitHub Actions 自动生成</p>
        </div>
    </footer>

    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute("data-theme");
            const newTheme = currentTheme === "light" ? "dark" : "light";
            html.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateThemeButton(newTheme);
        }

        function updateThemeButton(theme) {
            const icon = document.getElementById("theme-icon");
            const text = document.getElementById("theme-text");
            if (theme === "light") {
                icon.textContent = "☀️";
                text.textContent = "浅色";
            } else {
                icon.textContent = "🌙";
                text.textContent = "深色";
            }
        }

        (function() {
            const savedTheme = localStorage.getItem("theme") || "dark";
            document.documentElement.setAttribute("data-theme", savedTheme);
            updateThemeButton(savedTheme);
        })();
    </script>
</body>
</html>"""

    def generate_index(self, news_dir: Path) -> str:
        html_files = sorted(
            news_dir.glob("*.html"),
            key=lambda x: x.stem,
            reverse=True,
        )
        html_files = [f for f in html_files if f.name != "index.html"]

        items = []
        for html_file in html_files[:30]:
            date_str = html_file.stem
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                date_display = date_obj.strftime("%Y年%m月%d日")
                weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][
                    date_obj.weekday()
                ]
            except ValueError:
                date_display = date_str
                weekday = ""

            items.append(f'''
            <a href="{date_str}.html" class="archive-card">
                <div class="archive-date">
                    <span class="date-num">{date_str.split("-")[2]}</span>
                    <span class="date-month">{date_str.split("-")[1]}月</span>
                </div>
                <div class="archive-info">
                    <h3>{date_display}</h3>
                    <span class="weekday">{weekday}</span>
                </div>
                <span class="arrow">→</span>
            </a>''')

        return self._get_index_template().format(items="\n".join(items))

    def _get_index_template(self) -> str:
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技新闻日报 - 历史归档</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📁</text></svg>">
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent: #58a6ff;
            --accent-hover: #79b8ff;
            --border: #30363d;
            --shadow: rgba(0, 0, 0, 0.3);
        }

        [data-theme="light"] {
            --bg-primary: #f6f8fa;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --text-primary: #24292f;
            --text-secondary: #57606a;
            --text-muted: #8c959f;
            --accent: #0969da;
            --accent-hover: #0550ae;
            --border: #d0d7de;
            --shadow: rgba(0, 0, 0, 0.1);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }

        .container { max-width: 800px; margin: 0 auto; padding: 0 20px; }

        header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 20px 0;
            text-align: center;
        }

        h1 { font-size: 24px; margin-bottom: 8px; }

        .subtitle { color: var(--text-secondary); font-size: 14px; }

        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            z-index: 100;
        }

        .theme-toggle:hover { background: var(--border); }

        main { padding: 30px 0; }

        .archive-list { display: grid; gap: 12px; }

        .archive-card {
            display: flex;
            align-items: center;
            gap: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 20px;
            text-decoration: none;
            transition: all 0.2s;
        }

        .archive-card:hover {
            border-color: var(--accent);
            transform: translateX(5px);
        }

        .archive-date {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 50px;
        }

        .date-num { font-size: 28px; font-weight: 700; color: var(--accent); line-height: 1; }
        .date-month { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

        .archive-info { flex: 1; }
        .archive-info h3 { font-size: 16px; color: var(--text-primary); }
        .weekday { font-size: 13px; color: var(--text-muted); }

        .arrow { color: var(--text-muted); font-size: 18px; }

        footer {
            text-align: center;
            padding: 30px 0;
            color: var(--text-muted);
            font-size: 13px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📁 历史归档</h1>
            <p class="subtitle">科技新闻日报存档</p>
        </div>
    </header>

    <button class="theme-toggle" onclick="toggleTheme()">
        <span id="theme-icon">🌙</span>
        <span id="theme-text">深色</span>
    </button>

    <main class="container">
        <div class="archive-list">
            {items}
        </div>
    </main>

    <footer>
        <div class="container">
            <p>由 GitHub Actions 自动生成</p>
        </div>
    </footer>

    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute("data-theme");
            const newTheme = currentTheme === "light" ? "dark" : "light";
            html.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateThemeButton(newTheme);
        }

        function updateThemeButton(theme) {
            const icon = document.getElementById("theme-icon");
            const text = document.getElementById("theme-text");
            if (theme === "light") {
                icon.textContent = "☀️";
                text.textContent = "浅色";
            } else {
                icon.textContent = "🌙";
                text.textContent = "深色";
            }
        }

        (function() {
            const savedTheme = localStorage.getItem("theme") || "dark";
            document.documentElement.setAttribute("data-theme", savedTheme);
            updateThemeButton(savedTheme);
        })();
    </script>
</body>
</html>"""

    def get_filename(self) -> str:
        return f"news/{self.date_str}.html"
