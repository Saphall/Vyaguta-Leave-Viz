from typing import Optional
from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address

from .controller import fetch_departments_info

limiter = Limiter(key_func=get_remote_address)
departments_router = APIRouter()


@departments_router.get("/api/departments")
@limiter.limit("10/minute")
async def departments_info(
    request: Request,
    department_id: Optional[str] = Query(None, alias="department_id"),
):
    return await fetch_departments_info(request, department_id)
