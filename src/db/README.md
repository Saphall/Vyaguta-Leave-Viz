# DB

## Prerequisites

1. [Docker](https://docs.docker.com/)

## Setup

* **Setup PostgreSQL**

```powershell
docker compose up -d postgres
```

* **Synchronization**: This will create the necessary tables and procedures for the project.

```powershell
python setupdb.py --up
```

![image](https://github.com/user-attachments/assets/e92cbb90-ea7c-4400-99bb-29d3a246428f)

* **Rollback**: This will truncate all the tables and procedures created.

```powershell
python setupdb.py --down
```

![image](https://github.com/user-attachments/assets/7a01998f-c730-4333-bbce-273930b8182e)
