import scrapy

class ScrapyAppItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field() # Main extracted text content
    html_content = scrapy.Field() # Full HTML content