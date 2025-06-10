# Use a more general Debian-based image that often has better compatibility with system deps
# python:3.9-slim-bookworm is Debian 12
FROM python:3.9-slim-bookworm

# Set the working directory
WORKDIR /app

# Set environment variables for Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright/
ENV DEBIAN_FRONTEND=noninteractive

# Install core system dependencies required by Playwright
# and then allow 'playwright install' to handle the rest.
# These are the absolute minimum common deps for browser engines on Debian.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        # Core libraries for graphics, fonts, etc.
        ca-certificates \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libcurl4 \
        libdrm2 \
        libexpat1 \
        libgbm1 \
        libglib2.0-0 \
        libnspr4 \
        libnss3 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libstdc++6 \
        libx11-6 \
        libxcomposite1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxkbcommon0 \
        libxrandr2 \
        libxshmfence-dev \
        # Development tools for compilation if needed
        build-essential \
        # For curl and git
        curl \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- ADD THIS SECTION FOR NLTK DATA DOWNLOAD ---
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
# If you want to download to a specific path for NLTK, you could add:
# ENV NLTK_DATA=/usr/local/nltk_data
# RUN python -m nltk.downloader -d /usr/local/nltk_data punkt stopwords
# Then ensure your Python code looks in NLTK_DATA or a path in nltk.data.path

# Install Playwright browsers manually after system deps
# This command specifically downloads the browser binaries.
RUN playwright install chromium firefox webkit

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
