# =============================================================================
# NLP2CMD - Multi-stage Dockerfile
# =============================================================================
# Stage 1: Builder - install dependencies and build package
# Stage 2: Runtime - minimal image for running the application
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
FROM python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /build

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

# Install the package and dependencies
RUN pip install --user -e ".[dev]"

# -----------------------------------------------------------------------------
# Stage 2: Runtime
# -----------------------------------------------------------------------------
FROM python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a as runtime

# Labels
LABEL maintainer="NLP2CMD Team" \
    version="0.2.0" \
    description="Natural Language to Domain-Specific Commands Framework"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PATH="/root/.local/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # For shell commands testing
    findutils \
    grep \
    # For healthcheck
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash nlp2cmd

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY --chown=nlp2cmd:nlp2cmd src/ ./src/
COPY --chown=nlp2cmd:nlp2cmd examples/ ./examples/
COPY --chown=nlp2cmd:nlp2cmd tests/ ./tests/
COPY --chown=nlp2cmd:nlp2cmd pyproject.toml README.md LICENSE ./

# Install package in runtime
RUN pip install --no-cache-dir -e .

# Switch to non-root user
USER nlp2cmd

# Expose port for potential API server
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from nlp2cmd import get_registry; r = get_registry(); assert r.has('sql_select')" || exit 1

# Default command - run interactive CLI
CMD ["python", "-m", "nlp2cmd.cli"]

# -----------------------------------------------------------------------------
# Stage 3: Test runner (optional, for CI/CD)
# -----------------------------------------------------------------------------
FROM runtime as test

USER root

# Install test dependencies
RUN pip install --no-cache-dir pytest pytest-cov pytest-asyncio

USER nlp2cmd

# Run tests by default
CMD ["pytest", "tests/", "-v", "--tb=short"]
