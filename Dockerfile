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
# This list is now minimal, trusting Playwright's own installer for browser specifics.
# We update apt-get first to ensure we have the latest package lists
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        # Fundamental libraries for basic graphical applications/browsers
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
        libfontconfig1 \
        libfreetype6 \
        libicu-dev \
        # Build tools for Python packages and general utilities
        build-essential \
        curl \
        git \
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
# This command downloads the browser binaries. For system-level dependencies,
# it will attempt to install them via the system package manager if possible,
# or error out if not found. We've minimized our explicit list to avoid conflicts.
RUN playwright install chromium firefox webkit

# Copy the rest of the application code into the container
COPY . .

# Expose port 8080. This is the port your FastAPI application will listen on,
# and it should match the port you've configured Railway to expose.
EXPOSE 8080

# Command to run the FastAPI application using Uvicorn
# The application will listen on 0.0.0.0 (all interfaces) on port 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
