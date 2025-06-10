from scrapy import signals
from scrapy.http import HtmlResponse
from playwright.sync_api import sync_playwright
import time

class PlaywrightMiddleware:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch() # You can choose 'firefox' or 'webkit'

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def process_request(self, request, spider):
        if 'playwright' in request.meta and request.meta['playwright']:
            page = self.browser.new_page()
            try:
                page.goto(request.url)
                # You can add waits for specific elements or network idle
                # For dynamic content, waiting for a selector to appear is often better
                page.wait_for_load_state('networkidle') # Wait for network to be idle
                # You can also add a small fixed delay if dynamic content loads slowly
                # time.sleep(1)

                content = page.content()
                response = HtmlResponse(url=request.url, body=content, encoding='utf-8', request=request)
                return response
            except Exception as e:
                spider.logger.error(f"Playwright error for {request.url}: {e}")
                return None # Return None to fall back to default downloader or raise an error
            finally:
                page.close()
        return None # Let other middlewares or default downloader handle

    def spider_closed(self, spider):
        self.browser.close()
        self.playwright.stop()