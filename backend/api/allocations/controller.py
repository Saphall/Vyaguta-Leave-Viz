from fastapi import Request

from .services import fetch_filtered_allocations_info
from db.utils.database import databaseConnect, databaseDisconnect


async def fetch_allocations_info(
    request: Request,
    allocation_id: int,
):
    conn = await databaseConnect()

    try:
        if allocation_id:
            return await fetch_filtered_allocations_info(conn, allocation_id)
        return await fetch_filtered_allocations_info(conn)
    finally:
        await databaseDisconnect(conn)
