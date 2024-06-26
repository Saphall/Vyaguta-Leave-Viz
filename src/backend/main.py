import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.backend.api.routes import router
from src.backend.api.controller import load_leaves
from src.backend.error_handler.errors import rate_limit_handler


load_dotenv()
app = FastAPI()
app.include_router(router)
scheduler = AsyncIOScheduler()


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return await rate_limit_handler(request, exc)


@app.on_event("startup")
async def startup_event():
    scheduler.add_job(
        load_leaves, IntervalTrigger(seconds=12), args=[os.getenv("BEARER_TOKEN")]
    )
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.get("/")
async def index():
    return {"success": "Vyaguta Leave Info"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
