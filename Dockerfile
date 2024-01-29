FROM python:3.10.11-slim

ENV LC_ALL=C \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/home/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.0.10 \
    PYSETUP_PATH="/home/pysetup" \
    TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata"

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $PYSETUP_PATH

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    pkg-config \
    libpq-dev \
    libgl1-mesa-glx \
    libtesseract-dev \
    libleptonica-dev \
    vim \
    git \
    curl \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-lav \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY poetry.lock pyproject.toml ../
RUN poetry install --no-dev --no-ansi

WORKDIR /app

COPY app/ .

# Move traineddata files to $TESSDATA
COPY app/traineddata/ $TESSDATA_PREFIX

EXPOSE 8002
CMD ["make", "prod"]
