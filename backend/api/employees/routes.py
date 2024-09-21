from typing import Optional
from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address

from .controller import fetch_employee_info

limiter = Limiter(key_func=get_remote_address)
employee_router = APIRouter()


@employee_router.get("/api/employees")
@limiter.limit("10/minute")
async def employee_info(
    request: Request,
    employee_id: Optional[str] = Query(None, alias="employee_id"),
    designation_id: Optional[str] = Query(None, alias="designation_id"),
    department_id: Optional[str] = Query(None, alias="department_id"),
    team_manager_id: Optional[int] = Query(None, alias="team_manager_id"),
):
    return await fetch_employee_info(
        request, employee_id, designation_id, department_id, team_manager_id
    )
