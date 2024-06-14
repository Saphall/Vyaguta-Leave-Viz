# Backend

![FastAPI](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## Prerequisites

1. [GIT](https://git-scm.com/downloads)
2. [Pyenv](https://github.com/pyenv/pyenv#getting-pyenv)

## Installation

* Setup python

```zsh

pyenv update

sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev

pyenv install 3.11

pyenv local 3.11
```

* Install [Poetry](https://python-poetry.org/docs/)

* Use project environment using poetry

```zsh
poetry env use 3.11
```

* Activate virtual environment

```zsh
poetry shell
```

* Install dependencies

```zsh
poetry install
```

## Run locally

```zsh
uvicorn src.backend.main:app 
```
