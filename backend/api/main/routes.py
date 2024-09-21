from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from .controller import fetch_leaves, insert_leaves

limiter = Limiter(key_func=get_remote_address)
main_router = APIRouter()


@main_router.get("/")
async def index():
    return {
        "success": True,
        "message": "Vyaguta Leave Visualization System Backend",
        "endpoints": {
            "[GET] /vyaguta/api/leaves": "Fetch all the leave data from Vyaguta API",
            "[POST] /vyaguta/api/insert_leaves": "Insert leave data (JSON) obtained from Vyaguta into DB",
            "[GET] /api/employees": "Fetch all the employee Informations from Postgres DB",
            "[GET] /api/allocations": "Fetch all the employee allocations data from Postgres DB",
            "[GET] /api/departments": "Fetch all the departments data from Postgres DB",
            "[GET] /api/designations": "Fetch all the designations data from Postgres DB",
            "[GET] /api/fiscal_year": "Fetch all the fical_year data from Postgres DB",
            "[GET] /api/leave_types": "Fetch all the leave_types data from Postgres DB",
            "[GET] /api/leave_issuer": "Fetch all the leave_issuer data from Postgres DB",
            "[GET] /api/employee_leaves": "Fetch all the employee_leaves data from Postgres DB",
            "[GET] /api/leaves": "Fetch all the leave data from Postgres DB",
        },
    }


@main_router.get("/vyaguta/api/leaves")
@limiter.limit("5/minute")
async def vyaguta_leaves(request: Request):
    return await fetch_leaves(request)


@main_router.post("/vyaguta/api/insert_leaves")
async def load_vyaguta_leaves(request: Request):
    return await insert_leaves(request)
