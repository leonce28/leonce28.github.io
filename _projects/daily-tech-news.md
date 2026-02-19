---
layout: page
title: Daily Tech News
icon: 📰
description: 自动抓取每日科技新闻，生成静态页面
tech: Python
stars: 1
github: https://github.com/leonce28/leonce28.github.io
---

## 项目简介

Daily Tech News 是一个自动化的科技新闻聚合工具，每日定时抓取多个科技媒体的热门新闻，并生成美观的静态页面。

## 功能特点

- 🤖 **自动化抓取** - 使用 GitHub Actions 每日自动运行
- 📰 **多源聚合** - 支持 Hacker News、36氪、InfoQ、少数派
- 🎨 **精美页面** - 现代化设计，支持深色/浅色主题
- 📱 **响应式** - 完美适配各种设备
- 🔄 **反爬机制** - 随机 UA、延时、重试，稳定可靠

## 技术栈

- **Python 3.11** - 爬虫脚本
- **Jekyll** - 静态网站生成
- **GitHub Actions** - 自动化部署
- **SCSS** - 样式预处理

## 项目结构

```
daily-tech-news/
├── src/              # Python 爬虫代码
│   ├── scrapers/     # 各网站的爬虫
│   ├── generator.py  # Markdown 生成器
│   └── main.py       # 主程序
├── _news/            # Jekyll 新闻集合
├── _posts/           # 博客文章
├── _layouts/         # 页面布局
└── .github/          # GitHub Actions 配置
```

## 如何使用

1. Fork 本仓库
2. 启用 GitHub Actions
3. 启用 GitHub Pages
4. 等待自动运行或手动触发

## 查看效果

- [在线预览](https://leonce28.github.io)
- [源码地址](https://github.com/leonce28/leonce28.github.io)

欢迎 Star 和 Fork！⭐
