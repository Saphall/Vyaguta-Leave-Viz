FROM python:3.11.3-slim-buster as base

WORKDIR /app

# Setup dependencies for pyodbc
RUN \
  export ACCEPT_EULA='Y' && \
  # Install build dependencies
  apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https libcurl4 && \
  # Install pyodbc db drivers for MSSQL
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  apt-get update && \
  apt-get install -y msodbcsql17 && \
  apt-get remove -y curl apt-transport-https debconf-utils g++ gcc rsync unixodbc-dev build-essential gnupg2 && \
  apt-get autoremove -y && apt-get autoclean -y


  # Setup codebase
COPY ../../pyproject.toml ./
COPY ../../poetry.lock ./
COPY ../../README.md ./
COPY ../../LICENSE.md ./
COPY . .

RUN pip3 install poetry && \
  poetry config virtualenvs.create false


RUN poetry install

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
