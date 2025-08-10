ARG PYTHON_VERSION="3.10.14"

# Set build argument to use .python-version file if it exists, or default version
# ARG PYTHON_VERSION=${PYTHON_VERSION:-$(cat .python-version)}
ARG POETRY_VERSION="1.8.4"

# Use specified Python version or default version
FROM python:${PYTHON_VERSION}-bookworm AS base

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
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    TZ=UTC \
    TESSDATA_PREFIX="/usr/share/tesseract-ocr/5.00/tessdata"

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
    libcairo2-dev \
    liblept5 \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install packages
COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

FROM base AS builder

# Move traineddata files to $TESSDATA
ARG CACHE_BUST=1
COPY traineddata/ $TESSDATA_PREFIX
COPY ./app .

EXPOSE 8002

CMD poetry run alembic upgrade head && poetry run python main.py --log-level debug
