# Vyaguta Leave Viz

Visualize the Vyaguta Leave Information for Leapfrog employees over time.

```.
vyagutaviz
|
├── .github/                   # CI/CD scripts
|
├── src/
│   ├── backend/               # Contains code for Backend (API)
│   │   
│   ├── db/                    # Contains code for Database
│   │   ├── setupdb.py            
│   │   └── sql/
│   │       ├── migrations/
│   │       └── procedures/
|   |
│   ├── insights/              # Contains code for Visualization
│   │   └── #
|   |
│   └── utils/                 # Utilities files
│       └── db.py
|
├── tests/                     # Test Scripts
|
├── .pylintrc                  # Lint Check for Python files
|
├── .sqlfluff                  # Linter for SQL files
|
├── test.sh                    # Bash Script to test the code
|
├── docker-compose.yml         # Docker Compose file
|
└── pyproject.toml             # Package Manager
```

## [Backend](./src/backend/)

```zsh
uvicorn src.backend.main:app --reload
```

## [DB](./src/db/)

```zsh
docker compose up -d postgres
python src/db/setupdb.py --up
```

## [Insights](./src/insights/)

```zsh
streamlit run src/insights/dashboard.py
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
