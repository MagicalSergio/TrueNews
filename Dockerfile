FROM python:3.13-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync
RUN uv run playwright install chrome
RUN apt-get update
RUN apt-get install -y xvfb xserver-xephyr tigervnc-standalone-server x11-utils gnumeric 
