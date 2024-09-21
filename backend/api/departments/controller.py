from fastapi import Request

from .services import fetch_filtered_departments_info
from db.utils.database import databaseConnect, databaseDisconnect


async def fetch_departments_info(
    request: Request,
    department_id: int,
):
    conn = await databaseConnect()

    try:
        if department_id:
            return await fetch_filtered_departments_info(conn, department_id)
        return await fetch_filtered_departments_info(conn)
    finally:
        await databaseDisconnect(conn)
