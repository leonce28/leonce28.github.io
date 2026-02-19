# AGENTS.md

本项目是一个自动化的科技新闻抓取系统和个人博客网站，基于 Jekyll + Chirpy 主题构建，部署在 GitHub Pages。

## 项目概述

- **网站标题**: 撑花儿
- **作者名**: 撑花儿
- **URL**: https://leonce28.github.io
- **功能**: 每日自动抓取 Hacker News、36氪、InfoQ、少数派的热门科技新闻

## 技术栈

### 博客 (Jekyll)
- **主题**: jekyll-theme-chirpy
- **语言**: zh-CN (中文)
- **时区**: Asia/Shanghai
- **Ruby 依赖**: 见 `Gemfile`

### 爬虫 (Python)
- **版本**: Python 3.11+
- **依赖**: requests, lxml
- **安装**: `pip install -r requirements.txt`

## 目录结构

```
├── _config.yml           # Jekyll 主配置
├── _posts/               # 博客文章 (包含每日新闻)
├── _tabs/                # 页面 (about, projects, archives 等)
├── _data/
│   ├── locales/zh-CN.yml # 中文翻译覆盖
│   ├── contact.yml       # 社交链接
│   └── share.yml         # 分享配置
├── _includes/
│   └── metadata-hook.html # 自定义 head 注入 (JS/CSS)
├── assets/
│   ├── img/avatar.png    # 用户头像
│   └── js/quotes.js      # 自定义 JavaScript
├── src/                  # Python 爬虫代码
│   ├── main.py           # 主入口
│   ├── jekyll_generator.py # Jekyll 新闻文章生成器
│   └── scrapers/         # 各来源爬虫实现
│       ├── base.py       # 基类 (包含通用 RSS 逻辑)
│       ├── utils.py      # RequestHelper 工具类
│       ├── hackernews.py # Hacker News API 爬虫
│       ├── kr36.py       # 36氪 RSS 爬虫
│       ├── infoq.py      # InfoQ RSS 爬虫
│       └── sspai.py      # 少数派 RSS 爬虫
└── .github/workflows/
    ├── daily-news.yml    # 每日新闻抓取
    └── pages.yml         # GitHub Pages 部署
```

## 关键约定

### 博客文章格式

```yaml
---
title: "文章标题"
date: 2026-02-19 12:00:00 +0800
categories: [Category]
tags: [tag1, tag2]
description: "文章描述"
author: 撑花儿
---
```

### 每日新闻文章

- 文件名: `_posts/YYYY-MM-DD-daily-tech-news.md`
- Tags: `[news, daily-news]`
- Category: `News`
- 包含 `pin: true` 置顶

### 自定义内容注入

- **自定义 CSS/JS**: 编辑 `_includes/metadata-hook.html`
- **自定义翻译**: 编辑 `_data/locales/zh-CN.yml`
- **社交链接**: 编辑 `_data/contact.yml`

## 代码风格

### Python
- 使用类型注解: `def func(name: str) -> List[NewsItem]:`
- 类名: PascalCase (如 `HackerNewsScraper`)
- 函数/变量: snake_case (如 `get_news`)
- 常量: UPPER_SNAKE_CASE (如 `MAX_SUMMARY_LENGTH`)
- 导入顺序: 标准库 → 第三方库 → 本地模块

### Jekyll/Liquid
- Front matter 使用 YAML 格式
- 中文内容，保留专有名词英文

## 工作流程

### 修改后推送

**重要**: 每次完成文件修改后，必须将更改推送到远程仓库，以触发 GitHub Actions 自动部署。

```bash
git add .
git commit -m "描述修改内容"
git push origin master
```

推送后 GitHub Actions 会自动构建并部署到 https://leonce28.github.io

### 本地预览博客
```bash
bundle install
bundle exec jekyll serve
# 访问 http://127.0.0.1:4000
```

### 手动运行爬虫
```bash
pip install -r requirements.txt
python src/main.py
```

### Python 代码检查
```bash
ruff check src/
```

## 爬虫架构

```
BaseScraper (抽象基类，包含通用 RSS 抓取逻辑)
├── HackerNewsScraper  # 使用官方 API
├── Kr36Scraper        # RSS 订阅 (继承基类 RSS 逻辑)
├── InfoQScraper       # RSS 订阅 (继承基类 RSS 逻辑)
└── SspaiScraper       # RSS 订阅 (继承基类 RSS 逻辑)
```

### 核心类型
- **NewsItem**: TypedDict，统一新闻数据结构 (title, url, summary, score, comments, descendants)
- **RequestHelper**: HTTP 请求工具类，包含反爬机制
  - 随机 User-Agent
  - 请求延时
  - 指数退避重试
  - HTML 清理

## GitHub Actions

- **daily-news.yml**: 每日 UTC 0:00 (北京时间 8:00) 自动抓取新闻并提交
- **pages.yml**: 监听 master 分支推送，自动构建部署

## 排除文件

以下目录不会部署到 GitHub Pages (见 `_config.yml`):
- `src/` - Python 爬虫代码
- `vendor/` - Ruby 依赖
- `tools/` - 开发工具
- `requirements.txt`
- `Gemfile*`
