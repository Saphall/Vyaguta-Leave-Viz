from typing import Optional
from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address

from .controller import (
    fetch_leave_type_info,
    fetch_leave_issuer_info,
    fetch_employee_leaves_info,
    fetch_all_leave_info,
)

limiter = Limiter(key_func=get_remote_address)
leave_router = APIRouter()


@leave_router.get("/api/leave_types")
@limiter.limit("10/minute")
async def leave_type_info(
    request: Request,
    leave_type_id: Optional[str] = Query(None, alias="leave_type_id"),
):
    return await fetch_leave_type_info(request, leave_type_id)


@leave_router.get("/api/leave_issuer")
@limiter.limit("10/minute")
async def leave_issuer_info(
    request: Request,
    leave_issuer_id: Optional[str] = Query(None, alias="leave_issuer_id"),
):
    return await fetch_leave_issuer_info(request, leave_issuer_id)


@leave_router.get("/api/employee_leaves")
@limiter.limit("10/minute")
async def employee_leaves_info(
    request: Request,
    employee_id: Optional[str] = Query(None, alias="employee_id"),
    leave_type_id: Optional[str] = Query(None, alias="leave_type_id"),
    status: Optional[str] = Query(None, alias="status"),
    start_date: Optional[str] = Query(None, alias="start_date"),
    end_date: Optional[str] = Query(None, alias="end_date"),
    size: Optional[int] = Query(None, alias="size"),
):
    return await fetch_employee_leaves_info(
        request, employee_id, leave_type_id, status, start_date, end_date, size
    )


@leave_router.get("/api/leaves")
@limiter.limit("10/minute")
async def all_leave_info(
    request: Request,
    designation_id: Optional[str] = Query(None, alias="designation_id"),
    start_date: Optional[str] = Query(None, alias="start_date"),
    end_date: Optional[str] = Query(None, alias="end_date"),
    size: Optional[int] = Query(None, alias="size"),
):
    return await fetch_all_leave_info(
        request, designation_id, start_date, end_date, size
    )
