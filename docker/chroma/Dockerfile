FROM chromadb/chroma:latest

# Disable telemetry by default in this image
ENV ANONYMIZED_TELEMETRY=False

# Install curl for health checks
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
