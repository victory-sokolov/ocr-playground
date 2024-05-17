ARG DEFAULT_PYTHON_VERSION=3.10.14

# Set build argument to use .python-version file if it exists, or default version
ARG PYTHON_VERSION=${PYTHON_VERSION:-$(cat .python-version)}
ARG POETRY_VERSION="1.8.3"

# Use specified Python version or default version
FROM python:${PYTHON_VERSION:-${DEFAULT_PYTHON_VERSION}}-bullseye as builder

WORKDIR /ocr

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=250 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/home/poetry" \
    PYSETUP_PATH="/home/pysetup" \
    TESSDATA_PREFIX="/usr/share/tesseract-ocr/5.00/tessdata"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y \
    build-essential \
    pkg-config \
    liblept5 \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    libtool \
    libicu-dev \
    libcairo2-dev \
    tesseract-ocr-eng \
    tesseract-ocr-lav \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# Install packages
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-ansi --no-interaction

# Move traineddata files to $TESSDATA
COPY traineddata/ $TESSDATA_PREFIX
COPY . .

EXPOSE 8002

CMD poetry run alembic upgrade head && poetry run python main.py --log-level info
