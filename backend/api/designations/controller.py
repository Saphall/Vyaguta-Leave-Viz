from fastapi import Request

from .services import fetch_filtered_designations_info
from db.utils.database import databaseConnect, databaseDisconnect


async def fetch_designations_info(
    request: Request,
    designation_id: int,
):
    conn = await databaseConnect()

    try:
        if designation_id:
            return await fetch_filtered_designations_info(conn, designation_id)
        return await fetch_filtered_designations_info(conn)
    finally:
        await databaseDisconnect(conn)
