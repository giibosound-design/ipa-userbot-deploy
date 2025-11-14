FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Go
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    zip \
    unzip \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Go for building ipapatch
RUN wget -q https://go.dev/dl/go1.21.5.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz && \
    rm go1.21.5.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY tools/ ./tools/
COPY blatantsPatch.dylib .

# Build ipapatch from source
RUN cd tools/ipapatch && \
    go build -o ipapatch . && \
    chmod +x ipapatch && \
    cd /app

# Create temp directory
RUN mkdir -p /tmp/ipa_bot

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Create startup script that restores session
RUN echo '#!/bin/bash\n\
if [ ! -z "$SESSION_FILE_B64" ]; then\n\
  echo "Restoring session file..."\n\
  echo "$SESSION_FILE_B64" | base64 -d > /app/ipa_userbot_session.session\n\
  echo "✓ Session restored"\n\
fi\n\
python -m app.main' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]
