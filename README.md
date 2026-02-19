# 科技新闻日报

自动抓取每日科技新闻，生成 Markdown 文档。

## 新闻来源

- [Hacker News](https://news.ycombinator.com/) - 全球最大科技社区
- [36氪](https://36kr.com/) - 中文科技媒体
- [InfoQ](https://www.infoq.cn/) - 技术资讯平台
- [少数派](https://sspai.com/) - 高质量应用推荐

## 自动运行

- 每天北京时间 8:00 自动运行（UTC 0:00）
- 生成文件: `news/YYYY-MM-DD.md`
- 支持手动触发: Actions → Daily Tech News → Run workflow

## 本地运行

```bash
pip install -r requirements.txt
python src/main.py
```

## 项目结构

```
daily-tech-news/
├── .github/workflows/daily-news.yml
├── src/
│   ├── scrapers/          # 爬虫模块
│   ├── generator.py       # Markdown 生成
│   └── main.py            # 主入口
├── news/                  # 新闻存档
├── requirements.txt
└── README.md
```
