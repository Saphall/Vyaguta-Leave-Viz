from typing import Optional
from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address
from .controller import fetch_leave_info

limiter = Limiter(key_func=get_remote_address)
insights_router = APIRouter()


@insights_router.get("/api/leaves")
@limiter.limit("5/minute")
async def leave_info(
    request: Request,
    designationID: Optional[str] = Query(None, alias="designationID"),
    startDate: Optional[str] = Query(None, alias="startDate"),
    endDate: Optional[str] = Query(None, alias="endDate"),
    size: Optional[int] = Query(None, alias="size"),
):
    return await fetch_leave_info(request, designationID, startDate, endDate, size)
