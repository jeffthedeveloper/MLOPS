# ===============================
# Stage 1: Build base with dependencies
# ===============================
FROM python:3.8-slim-buster AS base

# Evita prompts interativos durante apt-get
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instala dependências do sistema de forma segura
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libopenblas-dev \
        libomp-dev \
        curl \
        git \
        apt-utils \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN useradd --create-home appuser
USER appuser

# Diretórios de cache do Hugging Face
ENV TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface \
    HF_HOME=/home/appuser/.cache/huggingface

# Copia e instala dependências Python
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

# Pré-baixa DistilGPT2 para evitar cold-start
RUN python -c "\
from transformers import AutoTokenizer, AutoModelForCausalLM; \
MODEL_NAME='distilgpt2'; \
AutoTokenizer.from_pretrained(MODEL_NAME); \
AutoModelForCausalLM.from_pretrained(MODEL_NAME); \
print('Prefetched model:', MODEL_NAME)\
"

# ===============================
# Stage 2: Final lean image
# ===============================
FROM python:3.8-slim-buster

WORKDIR /app

# Copia usuário e caches
COPY --from=base /etc/passwd /etc/passwd
COPY --from=base /etc/group /etc/group
COPY --from=base /home/appuser /home/appuser

# Copia pacotes Python instalados
COPY --from=base /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Copia arquivos da aplicação
COPY --chown=appuser:appuser . .

# Usa usuário não-root
USER appuser

# Porta exposta
EXPOSE 5000

# Variáveis de ambiente, já configuradas para DistilGPT2
ENV PATH="/home/appuser/.local/bin:$PATH" \
    TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface \
    HF_HOME=/home/appuser/.cache/huggingface \
    MODEL_NAME="distilgpt2" \
    MAX_NEW_TOKENS=120 \
    TEMPERATURE=0.8 \
    TOP_P=0.95 \
    NO_REPEAT_NGRAM=2

# Inicialização do Gunicorn
CMD ["gunicorn", "--workers=2", "--threads=2", "--timeout=180", "--bind", "0.0.0.0:5000", "app:app"]
