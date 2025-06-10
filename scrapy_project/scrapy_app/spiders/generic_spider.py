import scrapy
from bs4 import BeautifulSoup
import re

class GenericSpider(scrapy.Spider):
    name = 'generic_spider'

    def __init__(self, *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')] # Get URL from argument

    def start_requests(self):
        # Yield a standard Scrapy Request. No Playwright needed.
        self.logger.info(f"Starting request for: {self.start_urls[0]}")
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # Check if the request was successful
        if response.status != 200:
            self.logger.error(f"Failed to fetch {response.url}: Status {response.status}")
            # You might want to yield an item with an error status or raise an exception
            return

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else 'No title found'

        # Extract main content
        # This is a generic approach; you might need to refine it for specific websites.
        # It attempts to get text from common content-holding elements.
        content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div'])
        
        content_parts = []
        for element in content_elements:
            # Get text and strip whitespace, use a space as separator for internal tags
            text = element.get_text(separator=' ', strip=True)
            if text:
                content_parts.append(text)
        
        full_content = " ".join(content_parts)
        
        # Further clean up content: replace multiple spaces with single, remove excessive newlines/tabs
        full_content = re.sub(r'\s+', ' ', full_content).strip()
        full_content = re.sub(r'[\n\t\r]', ' ', full_content).strip()

        self.logger.info(f"Successfully scraped content from {response.url}")

        yield {
            'url': response.url,
            'title': title,
            'content': full_content,
            # 'beautified_content' will now just be the content extracted by BeautifulSoup
            # If you need raw HTML, you'd collect specific soup.find_all results as strings.
            # For simplicity, we'll assume the full_content is sufficient for 'beautified_content' in this context.
            'beautified_content': [{'title': title, 'content': full_content}]
        }
