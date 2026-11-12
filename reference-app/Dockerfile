# Stage 1: Build dependencies using uv
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project --no-dev --no-config --index-url https://pypi.org/simple

COPY main.py ./
COPY static ./static

# Stage 2: Minimal non-root Google Distroless runtime
FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=builder /app/.venv/lib/python3.12/site-packages /app/site-packages
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/static /app/static

ENV PYTHONPATH="/app/site-packages" \
    PORT=8080

EXPOSE 8080
USER nonroot

CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
