from typing import Optional
from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address

from .controller import fetch_allocations_info

limiter = Limiter(key_func=get_remote_address)
allocations_router = APIRouter()


@allocations_router.get("/api/allocations")
@limiter.limit("10/minute")
async def allocations_info(
    request: Request,
    allocation_id: Optional[str] = Query(None, alias="allocation_id"),
):
    return await fetch_allocations_info(request, allocation_id)
