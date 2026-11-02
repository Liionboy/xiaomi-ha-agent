ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM $BUILD_FROM

# Install Python & dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    && pip3 install --no-cache-dir --break-system-packages \
    fastapi \
    uvicorn \
    httpx \
    pyyaml \
    pydantic \
    python-multipart \
    aiofiles \
    && apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo

# Create app directory
WORKDIR /app

# Copy application code
COPY app/ .
COPY scripts/ /scripts/

# Make scripts executable
RUN chmod +x /scripts/*.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import httpx; httpx.get('http://localhost:8100/health').raise_for_status()"

# Ensure we're in the right directory for imports
WORKDIR /app

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100", "--workers", "1"]
