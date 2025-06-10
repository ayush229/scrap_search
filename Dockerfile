# Use the full Debian 12 (Bookworm) Python image
# This image contains a much more complete set of system libraries than the 'slim' version,
# which is often necessary for headless browsers like Playwright's Chromium.
FROM python:3.9-bookworm

# Set the working directory inside the container
WORKDIR /app

# Set environment variables for Playwright and locale
# PLAYWRIGHT_BROWSERS_PATH ensures browsers are installed in a known location
# DEBIAN_FRONTEND=noninteractive prevents apt-get from asking interactive interactive questions
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright/
ENV DEBIAN_FRONTEND=noninteractive
# Set a consistent locale for the container environment
ENV LANG=C.UTF-8
# Set a consistent locale for all locale categories
ENV LC_ALL=C.UTF-8

# Install core system dependencies required by Playwright and other tools
# With a full base image, many dependencies are already present.
# We'll keep a minimal set of crucial ones and those often needed by Playwright directly.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        # Essential runtime dependencies for browsers (Chromium, Firefox, WebKit)
        # libicu-dev is crucial for harfbuzz
        libicu-dev \
        # Basic build tools for Python packages and general utilities
        build-essential \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data during the Docker build process
# This ensures 'punkt' and 'stopwords' are available when the application runs
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Install Playwright browsers (Chromium, Firefox, WebKit)
# This command downloads the browser binaries and *should* now find all necessary
# system dependencies within the more complete 'python:3.9-bookworm' environment.
RUN playwright install chromium firefox webkit

# Copy the rest of the application code into the container
COPY . .

# Expose port 8080. This is the port your FastAPI application will listen on,
# and it should match the port you've configured Railway to expose.
EXPOSE 8080

# Command to run the FastAPI application using Uvicorn
# The application will listen on 0.0.0.0 (all interfaces) on port 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
