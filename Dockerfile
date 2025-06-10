# Use a more general Debian-based image that often has better compatibility with system deps
FROM python:3.9-slim-bookworm # buster is old, bookworm is current stable Debian

# Set the working directory
WORKDIR /app

# Set environment variables for Playwright to ensure it doesn't try to auto-install (we'll do it manually)
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright/
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required by Playwright
# This is a comprehensive list, including those often missing in slim images.
# We also update apt-get first to ensure we have the latest package lists.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        # General dependencies
        build-essential \
        libstdc++6 \
        libgcc-s1 \
        libc6 \
        # Playwright browser dependencies (for Chromium, Firefox, WebKit)
        # These are common for Debian-based systems.
        # Chromium specific
        libatk-bridge2.0-0 \
        libcups2 \
        libdrm2 \
        libgbm1 \
        libgdk-pixbuf2.0-0 \
        libglib2.0-0 \
        libgtk-3-0 \
        libxcomposite1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxrandr2 \
        libxshmfence6 \
        libnss3 \
        libxkbcommon0 \
        libatspi2.0-0 \
        libva-drm2 \
        libva-x11-2 \
        libva2 \
        libegl1 \
        libharfbuzz-icu7 \
        libwoff1 \
        libpng16-16 \
        libwebp6 \
        libjpeg62-turbo \
        libfontconfig1 \
        libfreetype6 \
        libx11-6 \
        libxi6 \
        libpangocairo-1.0-0 \
        libpango-1.0-0 \
        libcairo2 \
        fonts-liberation \
        # Firefox specific (some overlap with Chromium)
        libdbus-glib-1-2 \
        libgconf-2-4 \
        libnotify4 \
        libsqlite3-0 \
        libxtst6 \
        # WebKit specific (some overlap)
        liblcms2-2 \
        libwebkit2gtk-4.0-37 \
        # Other potential useful libs (e.g. for video playback, fonts)
        libpulse0 \
        libgstreamer-plugins-base1.0-0 \
        libgstreamer1.0-0 \
        # Font related
        fonts-unifont \
        # Required for playwright-stealth and general web scraping
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers manually after system deps
# We specify the browser types to install.
RUN playwright install chromium firefox webkit

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
