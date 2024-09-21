from typing import Optional
from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address

from .controller import fetch_fiscal_year_info

limiter = Limiter(key_func=get_remote_address)
fiscal_year_router = APIRouter()


@fiscal_year_router.get("/api/fiscal_year")
@limiter.limit("10/minute")
async def employee_info(
    request: Request,
    fiscal_id: Optional[str] = Query(None, alias="fiscal_id"),
    start_date: Optional[str] = Query(None, alias="start_date"),
    end_date: Optional[str] = Query(None, alias="end_date"),
):
    return await fetch_fiscal_year_info(request, fiscal_id, start_date, end_date)
