from fastapi import Request

from .services import fetch_filtered_fiscal_year_info
from db.utils.database import databaseConnect, databaseDisconnect


async def fetch_fiscal_year_info(
    request: Request,
    fiscal_id: int,
    start_date: str,
    end_date: str,
):
    conn = await databaseConnect()

    try:
        if fiscal_id or start_date or end_date:
            return await fetch_filtered_fiscal_year_info(
                conn, fiscal_id, start_date, end_date
            )
        return await fetch_filtered_fiscal_year_info(conn)
    finally:
        await databaseDisconnect(conn)
