FROM python:3.11.3-slim-buster as base

WORKDIR /app

# Setup dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential libssl-dev \
  zlib1g-dev libbz2-dev \
  unixodbc-dev libcurl4\
  libreadline-dev libsqlite3-dev\
  llvm libncurses5-dev \
  libncursesw5-dev xz-utils tk-dev \
  libffi-dev liblzma-dev libpq-dev postgresql-client && \
  # Clean up unnecessary packages
  apt-get autoremove -y && apt-get autoclean -y && \
  rm -rf /var/lib/apt/lists/*

# Setup codebase
COPY . .

# Install poetry and project dependencies
RUN pip3 install --no-cache-dir poetry && \
  poetry config virtualenvs.create false && \
  python -m pip install -e . && \
  poetry install --no-root --no-dev

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Define commands for each service
# Backend command
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend command
CMD ["streamlit", "run", "insights/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
