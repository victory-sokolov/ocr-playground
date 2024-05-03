ARG DEFAULT_PYTHON_VERSION=3.10.14

# Set build argument to use .python-version file if it exists, or default version
ARG PYTHON_VERSION=${PYTHON_VERSION:-$(cat .python-version)}
ARG POETRY_VERSION="1.8.2"

# Use specified Python version or default version
FROM python:${PYTHON_VERSION:-${DEFAULT_PYTHON_VERSION}}-bullseye as builder

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=250 \
    POETRY_HOME="/home/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VERSION} \
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -


# Install packages
COPY pyproject.toml ./
RUN poetry install --only main --no-ansi --no-interaction

# Move traineddata files to $TESSDATA
COPY app/traineddata/ $TESSDATA_PREFIX
COPY . .

EXPOSE 8002

# CMD make migrate && make prod
CMD poetry run alembic upgrade head && poetry run uvicorn app.main:app --log-level info
