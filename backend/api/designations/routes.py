from typing import Optional
from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address

from .controller import fetch_designations_info

limiter = Limiter(key_func=get_remote_address)
designations_router = APIRouter()


@designations_router.get("/api/designations")
@limiter.limit("10/minute")
async def designations_info(
    request: Request,
    designation_id: Optional[str] = Query(None, alias="designation_id"),
):
    return await fetch_designations_info(request, designation_id)
