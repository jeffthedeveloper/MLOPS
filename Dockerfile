# Stage 1: Build base with dependencies
FROM python:3.8-slim-buster AS base

WORKDIR /app

# System deps that help torch/transformers
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential         libopenblas-dev         libomp-dev         && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd --create-home appuser
USER appuser

# Caches live here for the appuser
ENV TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface         HF_HOME=/home/appuser/.cache/huggingface

# Copy requirements and install
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --upgrade pip &&         pip install --no-cache-dir -r requirements.txt

# Pre-download DistilGPT2 to avoid cold-start network at runtime
RUN python - << 'PY'
from transformers import AutoTokenizer, AutoModelForCausalLM
m = 'distilgpt2'
AutoTokenizer.from_pretrained(m)
AutoModelForCausalLM.from_pretrained(m)
print('Prefetched model:', m)
PY

# Stage 2: Final lean image
FROM python:3.8-slim-buster

WORKDIR /app

# Copy user and caches
COPY --from=base /etc/passwd /etc/passwd
COPY --from=base /etc/group /etc/group
COPY --from=base /home/appuser /home/appuser

# Copy installed site-packages
COPY --from=base /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# App files
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 5000

ENV PATH="/home/appuser/.local/bin:$PATH"         TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface         HF_HOME=/home/appuser/.cache/huggingface         MODEL_NAME="distilgpt2"         MAX_NEW_TOKENS=120         TEMPERATURE=0.8         TOP_P=0.95         NO_REPEAT_NGRAM=2

# Gunicorn tuned for slow model cold starts
CMD ["gunicorn", "--workers=2", "--threads=2", "--timeout=180", "--bind", "0.0.0.0:5000", "app:app"]
