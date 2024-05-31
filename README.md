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
