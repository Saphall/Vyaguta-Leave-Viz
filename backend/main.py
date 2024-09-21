import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from backend.api.main.routes import main_router
from backend.api.leaves.routes import leave_router
from backend.api.employees.routes import employee_router
from backend.api.allocations.routes import allocations_router
from backend.api.departments.routes import departments_router
from backend.api.fiscal_year.routes import fiscal_year_router
from backend.api.designations.routes import designations_router

from backend.api.main.controller import insert_leaves
from backend.error_handler.errors import rate_limit_handler


load_dotenv()
app = FastAPI()
routers = [
    main_router,
    employee_router,
    allocations_router,
    departments_router,
    designations_router,
    fiscal_year_router,
    leave_router,
]
for router in routers:
    app.include_router(router)
scheduler = AsyncIOScheduler()


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return await rate_limit_handler(request, exc)


@app.on_event("startup")
async def startup_event():
    scheduler.add_job(
        insert_leaves,
        IntervalTrigger(seconds=300),
        args=[os.getenv("BEARER_TOKEN")],
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.remove_all_jobs()
    scheduler.shutdown()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
