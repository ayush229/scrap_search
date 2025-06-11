import scrapy
from scrapy_app.items import ScrapyAppItem
from bs4 import BeautifulSoup

class GenericSpider(scrapy.Spider):
    name = "generic_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        if start_url:
            self.start_urls = [start_url]
        else:
            raise ValueError("You must provide 'start_url' argument for the spider.")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'playwright': True})

    def parse(self, response):
        item = ScrapyAppItem()
        item['url'] = response.url
        item['html_content'] = response.text

        # Use BeautifulSoup to extract text content and title
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title_tag = soup.find('title')
        item['title'] = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Extract all visible text content
        # Remove script and style tags first
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()
        
        # Get text from body or whole document if no body
        text_content = soup.body.get_text(separator=' ', strip=True) if soup.body else soup.get_text(separator=' ', strip=True)
        item['content'] = text_content

        yield item
