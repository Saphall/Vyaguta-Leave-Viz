from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from .controller import fetch_leaves, insert_leaves

limiter = Limiter(key_func=get_remote_address)
main_router = APIRouter()


@main_router.get("/")
async def index():
    return {
        "success": True,
        "message": "Vyaguta Leave Visualization System Backend",
        "endpoints": {
            "[GET] /vyaguta/api/leaves": "Fetch all leave data from Vyaguta API",
            "[POST] /vyaguta/api/insert_leaves": "Insert leave data (JSON) obtained from Vyaguta into DB",
            "[GET] /api/leaves": "Get all the leave data from Postgres DB",
        },
    }


@main_router.get("/vyaguta/api/leaves")
@limiter.limit("5/minute")
async def vyaguta_leaves(request: Request):
    return await fetch_leaves(request)


@main_router.post("/vyaguta/api/insert_leaves")
async def load_vyaguta_leaves(request: Request):
    return await insert_leaves(request)
