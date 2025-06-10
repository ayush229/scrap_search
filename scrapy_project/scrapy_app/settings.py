# Scrapy settings for scrapy_app project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scrapy_app"

SPIDER_MODULES = ["scrapy_app.spiders"]
NEWSPIDER_MODULE = "scrapy_app.spiders"


# Obey robots.txt protocol
# IMPORTANT: For traditional scraping, it's generally good practice to OBEY robots.txt.
# If you *must* ignore it, change to False, but be aware of legal/ethical implications.
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4 # Adjust based on your system resources and target website politeness

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1 # Be polite to websites to avoid being blocked.

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# We are no longer using Playwright, so its middleware is removed.
# DOWNLOADER_MIDDLEWARES = {
#     "scrapy_app.middlewares.MyCustomDownloaderMiddleware": 543,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     "scrapy_app.pipelines.ScrapyAppPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set log level (INFO, DEBUG, ERROR, WARNING, CRITICAL)
LOG_LEVEL = "INFO" # Changed back to INFO from DEBUG to reduce log verbosity, as browser issues are gone.
