from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from .controller import fetch_leaves, load_leaves

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.get("/api/vyaguta/leaves")
@limiter.limit("5/minute")
async def vyaguta_leaves(request: Request):
    return await fetch_leaves(request)


@router.post("/api/vyaguta/insert_leaves")
async def load_vyaguta_leaves(request: Request):
    return await load_leaves(request)
