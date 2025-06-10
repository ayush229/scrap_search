# pipelines.py (Optional)
class ScrapyAppPipeline:
    def process_item(self, item, spider):
        # You could add post-processing here if needed,
        # but for this setup, we're returning raw content from the spider.
        return item