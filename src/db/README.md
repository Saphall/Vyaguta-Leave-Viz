# DB



## Prerequisites

1. [Docker](https://docs.docker.com/)

## Setup

* Setup PostgreSQL

```zsh
docker compose up -d postgres
```

* Synchronization

```zsh
python setupdb.py --up
```

* Rollback

```zsh
python setupdb.py --down
```
