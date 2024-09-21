from fastapi import Request
from db.utils.database import databaseConnect, databaseDisconnect
from .services import fetch_filtered_all_leave_info


async def fetch_leave_info(
    request: Request, designationID: str, startDate: str, endDate: str, size: int
):
    conn = await databaseConnect()

    try:
        if designationID or startDate or endDate or size:
            return await fetch_filtered_all_leave_info(
                conn, designationID, startDate, endDate, size
            )
        return await fetch_filtered_all_leave_info(conn)

    finally:
        await databaseDisconnect(conn)
