from slowapi import Limiter
from typing import List, Optional
from slowapi.util import get_remote_address
from fastapi import APIRouter, Request, Query

from .controller import (
    fetch_employee_details_insight,
    fetch_employee_leaves_insight,
    fetch_leave_balance_insight,
)

limiter = Limiter(key_func=get_remote_address)
employee_insight_router = APIRouter()


@employee_insight_router.get("/api/employee_details_insight")
@limiter.limit("50/minute")
async def employee_details(
    request: Request,
    employee_name: Optional[List[str]] = Query(None, alias="employee_name"),
    fiscal_year: Optional[List[str]] = Query(None, alias="fiscal_date"),
    start_date: Optional[str] = Query(None, alias="start_date"),
    end_date: Optional[str] = Query(None, alias="end_date"),
    size: Optional[int] = Query(None, alias="size"),
):
    return await fetch_employee_details_insight(
        request, employee_name, fiscal_year, start_date, end_date, size
    )


@employee_insight_router.get("/api/employee_leaves_insight")
@limiter.limit("50/minute")
async def employee_leave_info(
    request: Request,
    employee_name: Optional[List[str]] = Query(None, alias="employee_name"),
    fiscal_year: Optional[List[str]] = Query(None, alias="fiscal_date"),
    designation_name: Optional[List[str]] = Query(None, alias="designation_name"),
    department_name: Optional[List[str]] = Query(None, alias="department_name"),
    leave_type: Optional[List[str]] = Query(None, alias="leave_type"),
    status: Optional[List[str]] = Query(None, alias="leave_status"),
    start_date: Optional[str] = Query(None, alias="start_date"),
    end_date: Optional[str] = Query(None, alias="end_date"),
    size: Optional[int] = Query(None, alias="size"),
):
    return await fetch_employee_leaves_insight(
        request,
        employee_name,
        fiscal_year,
        designation_name,
        department_name,
        leave_type,
        status,
        start_date,
        end_date,
        size,
    )


@employee_insight_router.get("/api/employee_leave_balance_insight")
@limiter.limit("50/minute")
async def employee_leave_balance_info(
    request: Request,
    employee_name: Optional[List[str]] = Query(None, alias="employee_name"),
    leave_type: Optional[List[str]] = Query(None, alias="leave_type"),
    fiscal_year: Optional[List[str]] = Query(None, alias="fiscal_date"),
    start_date: Optional[str] = Query(None, alias="start_date"),
    end_date: Optional[str] = Query(None, alias="end_date"),
    size: Optional[int] = Query(None, alias="size"),
):
    return await fetch_leave_balance_insight(
        request, employee_name, leave_type, fiscal_year, start_date, end_date, size
    )
