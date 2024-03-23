ARG DEFAULT_PYTHON_VERSION=3.10.13

# Set build argument to use .python-version file if it exists, or default version
ARG PYTHON_VERSION=${PYTHON_VERSION:-$(cat .python-version)}
ARG POETRY_VERSION="1.8.2"

# Use specified Python version or default version
FROM python:${PYTHON_VERSION:-${DEFAULT_PYTHON_VERSION}}-bullseye as builder


ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=120 \
    POETRY_HOME="/home/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    PYSETUP_PATH="/home/pysetup" \
    TESSDATA_PREFIX="/usr/share/tesseract-ocr/5.00/tessdata"

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $PYSETUP_PATH

RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y \
    build-essential \
    pkg-config \
    liblept5 \
    libtesseract-dev \
    libleptonica-dev \
    git \
    curl \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-lav \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-ansi

COPY . .

# Move traineddata files to $TESSDATA
COPY app/traineddata/ $TESSDATA_PREFIX

EXPOSE 8002

CMD ["make", "prod"]
