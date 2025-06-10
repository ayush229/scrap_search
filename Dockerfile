# Use a slim Debian-based image for a smaller footprint, as we no longer need a headless browser
FROM python:3.9-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Set environment variables for locale (good practice)
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install only essential system dependencies:
# build-essential for compiling Python packages with C extensions (if any)
# curl and git for basic utilities
# locales for locale-gen (if needed, small)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        locales \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && locale-gen C.UTF-8

# Copy requirements file and install Python dependencies
# --no-cache-dir prevents pip from storing downloaded packages, reducing image size
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data during the Docker build process
# This ensures 'punkt' and 'stopwords' are available when the application runs
# These are typically small files.
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copy the rest of the application code into the container
# .dockerignore will prevent unnecessary files from being copied
COPY . .

# Expose port 8080. This is the port your FastAPI application will listen on.
EXPOSE 8080

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
