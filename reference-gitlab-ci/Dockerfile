# Stage 1: Build dependencies using uv (matching Debian 12 Python 3.11 ABI)
FROM python:3.11-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-install-project --no-dev

COPY main.py ./
COPY static ./static
RUN chmod -R a+rX /app

# Stage 2: Minimal non-root Google Distroless runtime (Debian 12 / Python 3.11)
FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --chown=nonroot:nonroot --from=builder /app/.venv/lib/python3.11/site-packages /app/site-packages
COPY --chown=nonroot:nonroot --from=builder /app/main.py /app/main.py
COPY --chown=nonroot:nonroot --from=builder /app/static /app/static

ENV PYTHONPATH="/app/site-packages" \
    PORT=8080

EXPOSE 8080
USER nonroot

CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
