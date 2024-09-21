from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from .controller import fetch_leaves, insert_leaves

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.get("/")
async def index():
    return {
        "success": True,
        "message": "Vyaguta Leave Visualization System Backend",
        "endpoints": {
            "GET /api/vyaguta/leaves": "Fetch all leave information",
            "POST /api/vyaguta/insert_leaves": "Insert the leave information",
        },
    }


@router.get("/vyaguta/api/leaves")
@limiter.limit("5/minute")
async def vyaguta_leaves(request: Request):
    return await fetch_leaves(request)


@router.post("/vyaguta/api/insert_leaves")
async def load_vyaguta_leaves(request: Request):
    return await insert_leaves(request)
