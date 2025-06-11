import scrapy
from scrapy_playwright.page import PageMethod
import re

class GenericSpider(scrapy.Spider):
    name = 'generic_spider'

    def __init__(self, *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')] # Get URL from argument

    def start_requests(self):
        self.logger.info(f"Starting Playwright request for: {self.start_urls[0]}")
        yield scrapy.Request(
            url=self.start_urls[0],
            meta=dict(
                playwright=True, # Enable Playwright for this request
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'body'), # Wait for the body to be loaded
                ],
                errback=self.errback, # Error callback
            ),
            callback=self.parse,
        )

    async def parse(self, response): # Use async def for Playwright responses
        self.logger.info(f"Successfully scraped content from {response.url} using Playwright.")

        # Get the page content after JavaScript execution
        page_content = await response.text() # This should be the rendered HTML

        # Use BeautifulSoup to parse the HTML content
        from bs4 import BeautifulSoup # Import locally for async compatibility if needed
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else 'No title found'

        # Extract main content
        content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div'])

        content_parts = []
        for element in content_elements:
            text = element.get_text(separator=' ', strip=True)
            if text:
                content_parts.append(text)

        full_content = " ".join(content_parts)

        # Further clean up content
        full_content = re.sub(r'\s+', ' ', full_content).strip()
        full_content = re.sub(r'[\n\t\r]', ' ', full_content).strip()

        yield {
            'url': response.url,
            'title': title,
            'content': full_content,
            'beautified_content': [{'title': title, 'content': full_content}] # Or more detailed if needed
        }

    async def errback(self, failure): # Error handling for Playwright requests
        self.logger.error(f"Playwright request failed: {failure.request.url} - {failure.value}")
        # You can decide how to handle failures, e.g., retry or log more details
