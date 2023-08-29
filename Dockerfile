FROM python:3.10-slim as builder

CMD ["python", "-c", "import os;print(os.getcwd())"]

# get updates
RUN apt-get update \
  && apt-get install -y \
  curl \
  build-essential \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# install poetry
ENV POETRY_VERSION=1.4.2
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION
ENV PATH /root/.local/bin:$PATH

# Copy poetry files into working directory
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# create venv
RUN python -m venv --copies /app/venv

# Install poetry env
RUN . /app/venv/bin/activate && poetry install --only main

# add code
COPY . ./

# run uvicorn
CMD ["/app/venv/bin/python", "-c", "import docker; print(docker.__version__)"]

FROM python:3.10-slim as deploy

COPY --from=builder /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

# Add code
WORKDIR /app
COPY . ./

# run uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]