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
ROBOTSTXT_OBEY = False # Typically set to False when using Playwright for dynamic content

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy_app.middlewares.PlaywrightMiddleware": 800, # Higher priority
}

# Playwright specific settings
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 20000, # 20 seconds timeout for browser launch
    "args": [
        "--no-sandbox", # Essential for running in Docker
        "--disable-setuid-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage", # Use /tmp instead of /dev/shm
        "--no-zygote", # Might help in some Docker environments
        "--single-process", # Might help with memory/CPU
        "--incognito", # Clean session
        "--window-size=1280,720" # Define a window size
    ]
}

# Default navigation timeout for Playwright pages
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000 # 30 seconds

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item_pipeline.html
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
LOG_LEVEL = "DEBUG" # Keep DEBUG for thorough logging
