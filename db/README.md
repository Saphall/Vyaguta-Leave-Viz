# DB

![Postgresql](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRFK4UmCV-4Y2Z8CEw8Pzkq3UV2y0uFJA7IA&s)

## Prerequisites

1. [Docker](https://docs.docker.com/)
2. [sync-db](https://github.com/leapfrogtechnology/sync-db/tree/master)

## Setup

* **Setup PostgreSQL**

```powershell
docker compose up -d postgres
```

## Migration

> Recommended: Ensure you have Node js >= 20.x and yarn installed on your system.
> This will run migrations and setup environment for running the script. For the local environment, you'll need to provide `.env` file.

* Install `sync-db`

```powershell
  npm install @leapfrogtechnology/sync-db
```

* Creating required migrations. e.g.

```powershell
  sync-db make create_table_raw_leave_info

  Created src\migrations\20240922043018_create_table_raw_leave_info.up.sql
  Created src\migrations\20240922043018_create_table_raw_leave_info.down.sql
  Done in 0.45s.
```

* Update the `sync-db.yml` file configuration.

* **Running migrations and synchronization**:

```powershell
  # Run migrations and synchronize your views, procedures and functions.
  sync-db synchronize

  # Run migrations only
  sync-db migrate-latest
```

![image](https://github.com/user-attachments/assets/27836d02-78c2-451e-9c70-0eaf7ed05c7a)

* **Rolling back migrations**

```powershell
  sync-db migrate-rollback
```

![image](https://github.com/user-attachments/assets/2ddef723-0a80-443f-8d42-39c1ca8947cc)

## Migration without versioning

Use the Python script to directly create and drop the entire DB without migration version control.

* **Synchronization**: This will create the necessary tables and procedures for the project.

```powershell
python setupdb.py --up
```

![image](https://github.com/user-attachments/assets/ce1794bd-6f81-4c57-a9b5-635eb2c39d14)

* **Rollback**: This will drop entire tables and procedures created.

```powershell
python setupdb.py --down
```

![image](https://github.com/user-attachments/assets/7a01998f-c730-4333-bbce-273930b8182e)

## ETL (Extract, Transform, Load)

The ETL is scheduled to run every **5 minutes**: [Scheduler](https://github.com/Saphall/Vyaguta-Leave-Viz/blob/2a17ccab61ea09285a0e611466a802bbdeb1e939/backend/main.py#L43-L52).

The leave data is `extracted` from Vyaguta API, `trasformed` and `loaded` in Postgres Database as defined in [procedures.json](./procedures.json).

![image](https://github.com/user-attachments/assets/a0bc2084-dd5f-4d7e-9a26-3168c812ec95)
