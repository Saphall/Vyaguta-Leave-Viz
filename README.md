# Vyaguta Leave Viz

Visualize the Vyaguta Leave Information for Leapfrog employees over time.

```.
Vyaguta Leave Viz
|
├── .github/                   # CI/CD scripts
│   └── workflow/
|
├── backend/                   # Contains code for Backend (API)
│   ├── api/                   # Different API routes and their services
│   ├── error_handler/
│   ├── utils/
│   ├── tests/
│   ├── main.py
│   ├── README.md
│   ├── Dockerfile
│   └── vyaguta_info_example.json
|
├── db/                        # Contains code for Database
│   ├── sql/
│   └── utils/
│   ├── setupdb.py
│   ├── README.md
│   ├── procedures.json
|
├── infra/                     # Contains code for Infrastructure setup
│   ├── main.tf
│   ├── providers.tf
│   ├── settings.tf
│   └── variables.tf
│   ├── terraform.tfvars
│   ├── README.md
|
├── insights/                  # Contains code for Visualization
│   └── utils/
│   ├── dashboard.py
│   ├── Dockerfile
│   ├── README.md
|
├── .env.example               # Example environment variables
|
├── .gitignore                 # Git ignore file
|
├── .pylintrc                  # Lint Check for Python files
|
├── .python-version            # Python version file
|
├── .sqlfluff                  # Linter for SQL files
|
├── docker-compose.yml         # Docker Compose file
|
├── LICENSE.md                 # License file
|
├── poetry.lock                # Poetry lock file
|
├── pyproject.toml             # Package Manager
|
├── README.md                  # Project README
|
├── SETUP.md                   # Setup instructions
|
└── test.sh                    # Bash Script to test the code
```

## [Infra](./infra/)

```bash
terraform init
terraform apply
```

## [Backend](./backend/)

```zsh
uvicorn backend.main:app --reload
```

## [DB](./db/)

```zsh
docker compose up -d postgres
python db/setupdb.py --up
```

## [Insights](./insights/)

```zsh
streamlit run insights/dashboard.py
```

## Test

```zsh
chmod +x test.sh
./test.sh
```

## Visualizations

![image](https://github.com/Saphall/Vyaguta-Leave-Viz/assets/66344649/acb3b542-c955-4dd9-8e26-f552e31a4bb6)

![image](https://github.com/Saphall/Vyaguta-Leave-Viz/assets/66344649/9ba03aa1-4c7d-44a2-aa34-12fe7a8500af)

![image](https://github.com/Saphall/Vyaguta-Leave-Viz/assets/66344649/c37d93ad-4d8e-43c6-85ae-8789747fdb68)

![image](https://github.com/Saphall/Vyaguta-Leave-Viz/assets/66344649/94fa46d0-92da-43bb-9520-3ca0a8e0f34d)
