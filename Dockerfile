# Stage 1: Build base with dependencies
FROM python:3.8-slim-buster AS base

# Switch to root to modify sources.list and install packages
USER root

WORKDIR /app

# Replace sources.list with the official archive for Debian Buster (EOL)
RUN echo "deb http://archive.debian.org/debian/ buster main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list

# Update, install dependencies, and clean up in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libopenblas-dev \
        libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Set environment variables for caching
ENV TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface \
    HF_HOME=/home/appuser/.cache/huggingface

# Copy and install Python requirements
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download the model to avoid cold starts
RUN python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; m='distilgpt2'; AutoModelForCausalLM.from_pretrained(m); AutoTokenizer.from_pretrained(m);"

# Stage 2: Final lean image
FROM python:3.8-slim-buster

WORKDIR /app

# Copy user and caches from the base stage
COPY --from=base /etc/passwd /etc/passwd
COPY --from=base /etc/group /etc/group
COPY --from=base /home/appuser /home/appuser
COPY --from=base /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Copy application files
COPY --chown=appuser:appuser . .

# Switch to the non-root user
USER appuser

EXPOSE 5000

# Set runtime environment variables
ENV PATH="/home/appuser/.local/bin:$PATH" \
    TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface \
    HF_HOME=/home/appuser/.cache/huggingface \
    MODEL_NAME="distilgpt2"

# Gunicorn tuned for low-memory environments
CMD ["gunicorn", "--workers=1", "--threads=2", "--timeout=180", "--bind", "0.0.0.0:5000", "app:app"]
