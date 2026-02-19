import random
import time
from typing import Dict, Optional
import requests


class AntiScraper:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    ]

    REFERERS = [
        "https://www.google.com/",
        "https://www.google.com.hk/",
        "https://www.bing.com/",
        "https://www.baidu.com/",
        "https://www.duckduckgo.com/",
        "https://news.ycombinator.com/",
        "https://www.github.com/",
    ]

    ACCEPT_LANGUAGES = [
        "zh-CN,zh;q=0.9,en;q=0.8",
        "en-US,en;q=0.9",
        "zh-CN,zh;q=0.9",
        "en-GB,en;q=0.9,zh-CN;q=0.8",
    ]

    @staticmethod
    def get_headers(extra_headers: Optional[Dict] = None) -> Dict[str, str]:
        headers = {
            "User-Agent": random.choice(AntiScraper.USER_AGENTS),
            "Referer": random.choice(AntiScraper.REFERERS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": random.choice(AntiScraper.ACCEPT_LANGUAGES),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers

    @staticmethod
    def random_delay(min_sec: float = 1.0, max_sec: float = 3.0) -> None:
        time.sleep(random.uniform(min_sec, max_sec))

    @staticmethod
    def fetch_with_retry(
        url: str,
        max_retries: int = 3,
        timeout: int = 15,
        extra_headers: Optional[Dict] = None,
    ) -> Optional[requests.Response]:
        for attempt in range(max_retries):
            try:
                AntiScraper.random_delay(0.5, 1.5)
                response = requests.get(
                    url,
                    headers=AntiScraper.get_headers(extra_headers),
                    timeout=timeout,
                )
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    wait_time = (2**attempt) + random.uniform(1, 3)
                    time.sleep(wait_time)
            except requests.exceptions.RequestException:
                wait_time = (2**attempt) + random.uniform(0.5, 1.5)
                time.sleep(wait_time)
        return None
