# Use a more general Debian-based image that often has better compatibility with system deps
# python:3.9-slim-bookworm is Debian 12 (current stable Debian)
FROM python:3.9-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Set environment variables for Playwright and locale
# PLAYWRIGHT_BROWSERS_PATH ensures browsers are installed in a known location
# DEBIAN_FRONTEND=noninteractive prevents apt-get from asking interactive questions
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright/
ENV DEBIAN_FRONTEND=noninteractive
# Set a consistent locale for the container environment
ENV LANG=C.UTF-8
# Set a consistent locale for all locale categories
ENV LC_ALL=C.UTF-8

# Install core system dependencies required by Playwright and other tools
# We update apt-get first to ensure we have the latest package lists
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        # Essential runtime dependencies for browsers (Chromium, Firefox, WebKit)
        # Sourced from Playwright's own Dockerfiles and common browser deps for Debian Bookworm
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
        libjpeg-turbo8 \
        libfontconfig1 \
        libfreetype6 \
        libgconf-2-4 \
        libncurses5 \
        libxtst6 \
        libpulse0 \
        libgstreamer-plugins-base1.0-0 \
        libgstreamer1.0-0 \
        libicu-dev \
        libvpx-dev \
        # For WebP support, libwebp-dev or simply trusting Playwright to find it
        # libwebp-dev \ # Let's try without this explicit one, as it might be pulled by others or managed by Playwright
        # Common build tools for Python packages with C extensions, or if Playwright needs to compile something
        build-essential \
        # For curl and git
        curl \
        git \
        # For locale generation (can sometimes be a silent failure cause for browsers)
        locales \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    # Generate locale (C.UTF-8 is common for containers, needs 'locales' package)
    && locale-gen C.UTF-8

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data during the Docker build process
# This ensures 'punkt' and 'stopwords' are available when the application runs
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Install Playwright browsers (Chromium, Firefox, WebKit)
# This command downloads the browser binaries into the container
RUN playwright install chromium firefox webkit

# Copy the rest of the application code into the container
COPY . .

# Expose port 8080. This is the port your FastAPI application will listen on,
# and it should match the port you've configured Railway to expose.
EXPOSE 8080

# Command to run the FastAPI application using Uvicorn
# The application will listen on 0.0.0.0 (all interfaces) on port 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
