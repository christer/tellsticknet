FROM docker.io/python:3.14-slim-bookworm

WORKDIR /app

RUN set -x \
    && apt-get update \
    && apt-get -y --no-install-recommends install dumb-init libsodium23 \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && useradd -M --home-dir /app tellstick

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-dev --no-install-project

COPY . ./

RUN uv sync --frozen --no-dev --no-editable

USER tellstick

ENTRYPOINT ["dumb-init", "--", "python3", "-m", "tellsticknet", "mqtt"]
