# 代码审查报告

## 概述

本报告对项目 `leonce28.github.io` 进行了全面代码审查，包括 Python 爬虫代码、Jekyll 配置和 GitHub Actions 工作流。发现多个需要改进的问题。

---

## 严重问题 (Critical)

### 1. 代码重复严重 - RSS 爬虫实现完全重复

**位置**: `src/scrapers/kr36.py`, `src/scrapers/infoq.py`, `src/scrapers/sspai.py`

**问题**: 三个文件的 `_fetch_via_rss()` 和 `_clean_html()` 方法实现完全相同，仅 URL 不同。

**建议**: 将共性代码提取到基类 `BaseScraper` 或混入类中：

```python
# 建议在 BaseScraper 中添加
def _fetch_via_rss(self, rss_url: str) -> List[Dict]:
    # 通用 RSS 抓取逻辑
    ...

def _clean_html(self, text: str) -> str:
    import re
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
```

---

### 2. RSS URL 可能失效

**位置**: 
- `src/scrapers/infoq.py:10` - `https://www.infoq.cn/feed`
- `src/scrapers/sspai.py:10` - `https://sspai.com/feed`

**问题**: 
- InfoQ 中国站点 (infoq.cn) 可能已停止运营或更改域名
- 少数派的 RSS 订阅可能已失效

**建议**: 
- 手动验证这些 URL 是否可访问
- 考虑添加 URL 可访问性检查，失败时给出明确错误提示

---

### 3. GitHub Actions 并发冲突风险

**位置**: `.github/workflows/daily-news.yml:40`

**问题**: 
```bash
git add .
git diff --quiet && git diff --staged --quiet || git commit -m "docs: add daily news $(date +'%Y-%m-%d')"
git push
```
如果工作流在同一天多次触发（如手动触发 + 定时触发），可能导致 push 冲突。

**建议**: 添加检查或使用 `--force-with-lease`:
```bash
git push --force-with-lease
```

---

## 改进建议 (Improvements)

### 4. AntiScraper 类命名误导

**位置**: `src/scrapers/utils.py:7`

**问题**: 类名 `AntiScraper` 暗示这是"反爬虫"功能，但实际是"伪装爬虫"。

**建议**: 重命名为 `RequestHelper` 或 `ScraperUtils`。

---

### 5. 静默失败 - 无错误日志

**位置**: 
- `src/scrapers/base.py:19-21`
- `src/scrapers/utils.py:70-86`

**问题**: 异常被捕获后仅打印简单消息，没有日志级别、请求 URL、状态码等信息。

**建议**: 改进日志记录：
```python
import logging
logger = logging.getLogger(__name__)

def fetch_with_retry(...):
    for attempt in range(max_retries):
        try:
            ...
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
```

---

### 6. main.py 生成未使用的文件

**位置**: `src/main.py:42-47`

**问题**: `MarkdownGenerator` 生成的文件路径为 `news/{date}.md`，但 `_config.yml` 的 `exclude` 列表已排除 `news/` 目录，该文件不会被部署。

**建议**: 
- 如果不需要 Markdown 版本，删除相关代码
- 或者修改 `_config.yml` 允许部署 news 目录

---

### 7. HTML Generator 未被使用

**位置**: `src/html_generator.py`

**问题**: 
- `HtmlGenerator` 类定义了完整的 HTML 生成逻辑
- `generate_index()` 方法从未被调用
- 超过 600 行代码，包含大量重复 CSS

**建议**: 
- 如果不需要独立 HTML 页面，删除整个文件
- 或者考虑将 CSS 提取到单独文件

---

### 8. 时区硬编码

**位置**: `src/jekyll_generator.py:11`

**问题**: 
```python
self.datetime_str = self.date_cn.strftime("%Y-%m-%d %H:%M:%S +0800")
```
时区偏移 `+0800` 硬编码。

**建议**: 使用 pytz 或 zoneinfo 获取正确时区：
```python
from zoneinfo import ZoneInfo
self.datetime_str = self.date_cn.strftime("%Y-%m-%d %H:%M:%S %z")
```

---

### 9. 类型注解不一致

**位置**: 各爬虫文件

**问题**: 返回的字典字段不统一：
- HackerNews 返回: `title, url, summary, score, comments, descendants`
- 其他爬虫只返回: `title, url, summary`

**建议**: 定义统一的数据类或 TypedDict：
```python
from typing import TypedDict

class NewsItem(TypedDict):
    title: str
    url: str
    summary: str
    score: Optional[int]
    comments: Optional[str]
    descendants: Optional[int]
```

---

### 10. GitHub Actions 冗余配置

**位置**: `.github/workflows/pages.yml:5-6`

**问题**: 
```yaml
branches:
  - main
  - master
```
仓库只有 `master` 分支，`main` 分支配置冗余。

---

### 11. Jekyll 配置空值过多

**位置**: `_config.yml`

**问题**: 大量空配置项（如 `twitter.username:`, `analytics.google.id:` 等），影响可读性。

**建议**: 删除未使用的配置项，或添加注释说明预留用途。

---

### 12. HTML 转义实现不完整

**位置**: `src/jekyll_generator.py:69-76`, `src/html_generator.py:77-84`

**问题**: 手动实现 HTML 转义，未处理 `&` 重复转义问题。

**建议**: 使用标准库：
```python
import html
def _escape_html(self, text: str) -> str:
    return html.escape(text)
```

---

## 次要问题 (Nitpicks)

### 13. 导入顺序不符合 PEP 8

**位置**: 多个 Python 文件

**问题**: 标准库和第三方库导入未分组。

**建议**:
```python
import re  # 标准库
from abc import ABC, abstractmethod  # 第三方
from typing import List, Dict  # 本地
```

---

### 14. 魔法数字

**位置**: 多处

**问题**: 使用硬编码数字如 `200`, `10`, `3` 等。

**示例**:
- `src/scrapers/hackernews.py:33`: `summary[:200] + "..."`
- `src/scrapers/utils.py:72`: `random_delay(0.5, 1.5)`

**建议**: 提取为常量：
```python
MAX_SUMMARY_LENGTH = 200
MIN_DELAY = 0.5
MAX_DELAY = 1.5
```

---

## 安全考虑

### 15. 缺少 SSL 验证选项

**位置**: `src/scrapers/utils.py:73`

**问题**: `requests.get()` 默认验证 SSL，但某些旧站点可能有问题。

**建议**: 如果需要，可添加选项（仅在必要时使用）：
```python
def fetch_with_retry(..., verify: bool = True):
    response = requests.get(..., verify=verify)
```

---

## 总结

| 类别 | 数量 |
|------|------|
| 严重问题 | 3 |
| 改进建议 | 9 |
| 次要问题 | 2 |
| 安全考虑 | 1 |

**建议优先级**:
1. 首先验证 RSS URL 是否可用
2. 消除代码重复（将 RSS 逻辑提取到基类）
3. 改进错误日志记录
4. 清理未使用的代码（HtmlGenerator、MarkdownGenerator 输出）
5. 修复 GitHub Actions 并发问题
