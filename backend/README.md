# Backend

<img src = 'https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png' width=30%>

Backend Setup for the Leave Vizualization system.

```bash
backend/
├── api/                            # Different API routes and their services
│   ├── allocations/                # API code for the allocation details
│   ├── departments/                # API code for the department details
│   └── designations/               # API code for the designation details
│   └── employees/                  # API code for the employee details
│   └── fiscal_year/                # API code for the fiscal_year details
│   └── insights/                   # API code for the insights
│   └── leaves/                     # API code for the leave details
│   └── main/                       # API code for the vyaguta API fetch/insert and cron job
├── error_handler/                  # Code to handle different errors
│   └──  errors.py
├── tests/                          # Unit and Functional test
│   ├── functional/
│   └── unit
├── utils/                          # Utility codes
├── main.py                         # Main file for backend
├── README.md
└── vyaguta_info_example.json       # Example leave data
```

## Run locally

```zsh
uvicorn backend.main:app --reload
```

## Using Docker

```bash
docker compose up -d backend
```

## API Endpoints

![image](https://github.com/user-attachments/assets/c816f8c6-a268-449f-831e-50025f94cb03)

* `[GET] /vyaguta/api/leaves`: Fetch all the leave data from Vyaguta API

* `[POST] /vyaguta/api/insert_leaves`: Insert leave data (JSON) obtained from Vyaguta into DB

* `[GET] /api/employees`: Fetch all the employee information from Postgres DB

* `[GET] /api/allocations`: Fetch all the employee allocations data from Postgres DB

* `[GET] /api/departments`: Fetch all the departments data from Postgres DB

* `[GET] /api/designations`: Fetch all the designations data from Postgres DB

* `[GET] /api/fiscal_year`: Fetch all the fical_year data from Postgres DB

* `[GET] /api/leave_types`: Fetch all the leave_types data from Postgres DB

* `[GET] /api/leave_issuer`: Fetch all the leave_issuer data from Postgres DB

* `[GET] /api/employee_leaves`: Fetch all the employee_leaves data from Postgres DB

* `[GET] /api/employee_details_insight`: Fetch all the employee details information from Postgres DB

* `[GET] /api/employee_leaves_insight`: Fetch all the employee leave insights data from Postgres DB

* `[GET] /api/employee_leave_balance_insight`: Fetch all the employee leave balance from Postgres D

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
