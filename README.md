# Vyaguta Leave Viz

Vyaguta Leave Viz is a web-based application that allows to manage and visualize employee leave data. It integrates with the Vyaguta API to fetch leave data and provides insights through various visualizations and reports. Users can also upload the leave data and visualize it. The visualization dashboard shows insights about the employees' leave trends.

* Data Upload and API Consumption
* Employee Profile Management
* Comprehensive Leave Data Visualization
* Real-time Data Updates
* Customizable Visualization Options
* Reporting and Insights
* Fiscal Year Configuration

## Project Structure

```bash
Vyaguta Leave Viz

├── .github/                   # CI/CD scripts
│   └── workflow/
├── backend/                   # Contains code for Backend (API)
│   ├── api/                   # Different API routes and their services
│   ├── error_handler/
│   ├── utils/
│   ├── tests/
│   ├── main.py
│   ├── README.md
│   ├── Dockerfile
│   └── vyaguta_info_example.json
├── db/                        # Contains code for Database
│   ├── src/
|       ├── migrations/
|       ├── sql/
│   └── utils/
│   ├── setupdb.py
│   ├── README.md
│   ├── procedures.json
├── infra/                     # Contains code for Infrastructure setup
│   ├── main.tf
│   ├── providers.tf
│   ├── settings.tf
│   └── variables.tf
│   ├── terraform.tfvars
│   ├── README.md
├── insights/                  # Contains code for Visualization
│   └── .streamlit/
│   └── assets/
│   └── page/
│   └── utils/
│   ├── app.py
│   ├── README.md
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
├── .pylintrc                  # Lint Check for Python files
├── .python-version            # Python version file
├── .sqlfluff                  # Linter for SQL files
├── docker-compose.yml         # Docker Compose file
├── LICENSE.md                 # License file
├── poetry.lock                # Poetry lock file
├── pyproject.toml             # Package Manager
├── README.md                  # Project README
└── test.sh                    # Bash Script to test the code
```

## Architecture Diagram

![Language Proficiency Architecture Diagram drawio](https://github.com/user-attachments/assets/58b8851f-fd57-4c01-9278-31e40c716ba4)

## Setup

### Prerequisites

1. [GIT](https://git-scm.com/downloads)
2. [Pyenv](https://github.com/pyenv/pyenv#getting-pyenv)

### Installation

* Setup python

    ```bash
    pyenv update

    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev libpq-dev

    pyenv install 3.11

    pyenv local 3.11
    ```

* Install [Poetry](https://python-poetry.org/docs/)

* Use project environment using poetry

    ```bash
    poetry env use 3.11
    ```

* Activate virtual environment

    ```bash
    poetry shell
    ```

* Install dependencies

    ```bash
    python -m pip install -e .
    poetry install
    ```

## Services

* ### [Infra](./infra/)

    ```bash
    terraform init
    terraform apply
    ```

* ### [DB](./db/)

    ```bash
    docker compose up -d postgres
    ```

    Run Migrartions

    ```bash
    python db/setupdb.py --up
    or 
    yarn sync-db synchronize
    ```

* ### [Backend](./backend/)

    ```bash
    docker compose up -d backend
    or 
    uvicorn backend.main:app --reload
    ```

* ### [Insights](./insights/)

    ```bash
    docker compose up -d frontend
    or
    streamlit run insights/app.py reload
    ```
  
## Run the system

```bash
docker compose up
```

![image](https://github.com/user-attachments/assets/96882ff8-281e-4c43-b504-8eacdcbacb41)

## Test

```bash
chmod +x test.sh
./test.sh
```

## Visualizations

  ![image](https://github.com/user-attachments/assets/aeeab170-7de6-49c4-ac68-d474bcf1112d)

* ### Overview Page

  ![image](https://github.com/user-attachments/assets/3ac4917e-7dc5-4427-9eaf-083bbb4a8859)

  ![image](https://github.com/user-attachments/assets/225f1943-fa2d-47da-b47a-f1cf5744dfbd)
  
  ![image](https://github.com/user-attachments/assets/9c22f174-7a4d-45aa-86a1-63f1b6b1f663)
  
  ![image](https://github.com/user-attachments/assets/5c6cf76d-92a3-43c2-bafc-59cc14a3ad3b)
  
  ![image](https://github.com/user-attachments/assets/5ade18a0-4457-46ea-87a8-24f17d06dec3)

* ### Employee Page

  ![image](https://github.com/user-attachments/assets/eda7bdcc-ff53-4541-98d1-e5f5e3e76d72)

  ![image](https://github.com/user-attachments/assets/d066a0e3-35c0-4619-ba15-f76655311c49)

* ### Leave Trends Page

  ![image](https://github.com/user-attachments/assets/d7c90623-471d-43c8-921f-e67c37566289)

  ![image](https://github.com/user-attachments/assets/77e68ebe-41ac-445e-8257-352c2c36328e)

* ### About

  ![image](https://github.com/user-attachments/assets/18f1b829-7fc2-4f69-a30b-b35fd446d96a)
