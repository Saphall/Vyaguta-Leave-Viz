# Backend

<img src = 'https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png' width=50%>

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
uvicorn backend.main:app --reload
```

## API Endpoints

![image](https://github.com/user-attachments/assets/ea4e997f-19e2-4cfc-9b38-975645704893)

* `[GET] /vyaguta/api/leaves`: Fetch all the leave data from Vyaguta API

* `[POST] /vyaguta/api/insert_leaves`: Insert leave data (JSON) obtained from Vyaguta into DB

* `[GET] /api/employees`: Fetch all the employee information from Postgres DB

* `[GET] /api/allocations`: "Fetch all the employee allocations data from Postgres DB"

* `[GET] /api/departments`: "Fetch all the departments data from Postgres DB"

* `[GET] /api/designations`: "Fetch all the designations data from Postgres DB"

* `[GET] /api/fiscal_year`: "Fetch all the fical_year data from Postgres DB"

* `[GET] /api/leave_types`: "Fetch all the leave_types data from Postgres DB"

* `[GET] /api/leave_issuer`: "Fetch all the leave_issuer data from Postgres DB"

* `[GET] /api/employee_leaves`: "Fetch all the employee_leaves data from Postgres DB"

* `[GET] /api/leaves`: Fetch all the leave information from Postgres DB

## Example API Call

Curl:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/designations?designation_id=4' \
  -H 'accept: application/json'
```

Request URL: 

```bash
http://127.0.0.1:8000/api/designations?designation_id=4
```

Response:

```json
{
  "data": [
    {
      "designation_id": 4,
      "designation_name": "Senior Software Engineer"
    },
    {
      "total_count": 1
    }
  ],
  "status_code": 200
}
```
