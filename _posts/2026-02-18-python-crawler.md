---
title: "Python 爬虫实战：自动抓取每日科技新闻"
date: 2026-02-18 10:00:00 +0800
categories: [Tutorial]
tags: [python, crawler, automation, github-actions]
description: "使用 Python 定时抓取科技新闻，并自动生成静态页面。"
author: 撑花儿
---

## 项目背景

每天打开电脑，第一件事就是浏览各大科技网站了解最新动态。但是逐个打开网站太麻烦了，不如写个爬虫自动抓取！

## 技术方案

### 爬虫部分

使用 Python 的 `requests` 和 `BeautifulSoup` 库进行网页抓取：

```python
import requests
from bs4 import BeautifulSoup

def fetch_news(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # 解析新闻内容...
    return news_list
```

### 反爬机制

为了避免被封禁，需要加入一些反爬措施：

- 随机 User-Agent
- 请求延时
- 失败重试

```python
import random
import time

USER_AGENTS = [
    'Mozilla/5.0 (Windows...)',
    'Mozilla/5.0 (Macintosh...)',
    # 更多 UA...
]

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS)
    }

def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=get_headers())
            if response.status_code == 200:
                return response
        except Exception:
            time.sleep(2 ** attempt)
    return None
```

### 自动化部署

使用 GitHub Actions 实现每日自动运行：

```yaml
name: Daily Tech News

on:
  schedule:
    - cron: '0 0 * * *'  # UTC 0:00 = 北京时间 8:00

jobs:
  fetch-news:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Fetch news
        run: python src/main.py
      - name: Commit changes
        run: |
          git config user.name "github-actions[bot]"
          git commit -am "docs: update news"
          git push
```

## 成果展示

项目已经运行起来了，每天自动抓取以下网站的热门新闻：

- Hacker News
- 36氪
- InfoQ
- 少数派

生成的新闻页面支持深色/浅色主题切换，响应式设计，体验不错！

## 源码地址

完整代码已经开源在 GitHub：

[https://github.com/leonce28/leonce28.github.io](https://github.com/leonce28/leonce28.github.io)

欢迎 Star ⭐
