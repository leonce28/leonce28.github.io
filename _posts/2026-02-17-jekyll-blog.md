---
title: "Jekyll 博客搭建指南"
date: 2026-02-17 10:00:00 +0800
categories: [Tutorial]
tags: [jekyll, github-pages]
description: "从零开始搭建一个漂亮的 Jekyll 博客。"
author: 撑花儿
---

## 为什么选择 Jekyll

Jekyll 是一个简单的静态网站生成器，非常适合用来搭建博客：

- **免费托管** - GitHub Pages 免费提供
- **简单易用** - Markdown 写文章
- **高度可定制** - 主题、插件丰富
- **SEO 友好** - 静态页面加载快

## 安装 Jekyll

### 环境要求

- Ruby 2.5+
- RubyGems
- GCC 和 Make

### 安装步骤

```bash
# 安装 Jekyll 和 Bundler
gem install jekyll bundler

# 创建新项目
jekyll new my-blog

# 进入目录
cd my-blog

# 启动本地服务器
bundle exec jekyll serve
```

打开浏览器访问 `http://localhost:4000` 即可预览。

## 目录结构

```
my-blog/
├── _config.yml      # 配置文件
├── _posts/          # 博客文章
├── _layouts/        # 布局模板
├── _includes/       # 可复用组件
├── _sass/           # 样式文件
├── assets/          # 静态资源
└── index.html       # 首页
```

## 写文章

在 `_posts` 目录下创建文件，命名格式为 `YYYY-MM-DD-title.md`：

```markdown
---
layout: post
title: "我的第一篇文章"
date: 2026-02-17
tags: [博客]
---

这是文章内容...
```

## 部署到 GitHub Pages

1. 创建 GitHub 仓库 `username.github.io`
2. 推送代码
3. 在仓库设置中启用 GitHub Pages
4. 访问 `https://username.github.io`

## 总结

Jekyll 是搭建个人博客的绝佳选择，结合 GitHub Pages 可以实现免费、稳定的博客服务。快去试试吧！
