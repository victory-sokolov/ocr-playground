ARG DEFAULT_PYTHON_VERSION=3.10.14

# Set build argument to use .python-version file if it exists, or default version
ARG PYTHON_VERSION=${PYTHON_VERSION:-$(cat .python-version)}
ARG POETRY_VERSION="1.8.3"

# Use specified Python version or default version
FROM python:${PYTHON_VERSION:-${DEFAULT_PYTHON_VERSION}}-bookworm AS base

WORKDIR /ocr

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    TZ=UTC

RUN rm -rf /var/lib/apt/lists/*
RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom

RUN apt-get clean \
    && apt-get update && apt-get upgrade -y \
    && apt-get install -y --fix-missing \
    build-essential \
    curl \
    pkg-config \
    libtool \
    libicu-dev \
    libcairo2-dev

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install packages
ARG INSTALL_DEV=false
COPY poetry.lock pyproject.toml ./
RUN bash -c "if [$INSTALL_DEV == 'true']; then poetry install --no-root ; else poetry install --no-root --only main; fi"

FROM base AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    TESSDATA_PREFIX="/usr/share/tesseract-ocr/5.00/tessdata"

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    liblept5 \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-lav

# Move traineddata files to $TESSDATA
ARG CACHE_BUST=1
COPY traineddata/ $TESSDATA_PREFIX
COPY ./app .

EXPOSE 8002

CMD poetry run alembic upgrade head && poetry run python main.py --log-level debug
