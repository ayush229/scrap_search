BOT_NAME = "scrapy_app"

SPIDER_MODULES = ["scrapy_app.spiders"]
NEWSPIDER_MODULE = "scrapy_app.spiders"

ROBOTSTXT_OBEY = False # Be cautious with this, but often necessary for scraping dynamic content

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4 # Adjust based on your system resources and target website

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1 # Be polite, especially with Playwright

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# DOWNLOADER_MIDDLEWARES = {
#     "scrapy_app.middlewares.PlaywrightMiddleware": 800, # Higher priority
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy_app.middlewares.PlaywrightMiddleware": 800, # Higher priority for Playwright to handle requests
}


# Configure item pipelines
# ITEM_PIPELINES = {
#     # "scrapy_app.pipelines.ScrapyAppPipeline": 300,
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

# Playwright settings
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True, # Set to False for debugging
    "timeout": 20000, # 20 seconds for browser launch
    "args": [
        "--no-sandbox",             # Crucial for Docker environments
        "--disable-setuid-sandbox", # Crucial for Docker environments
        "--disable-gpu",            # No GPU in typical Docker containers
        "--disable-dev-shm-usage",  # Use /tmp instead of /dev/shm for shared memory
        "--no-zygote",              # Sometimes helps with stability
        "--single-process",         # Simpler process model
        "--incognito",              # Start in incognito mode for clean sessions
        "--window-size=1280,720"     # Set a consistent window size
    ]
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000 # 30 seconds for page navigation (e.g., page.goto)

# Set log level (INFO, DEBUG, ERROR, WARNING, CRITICAL)
# CHANGED TO DEBUG for better visibility into scraping issues
LOG_LEVEL = "DEBUG"
