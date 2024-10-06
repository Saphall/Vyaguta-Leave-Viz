from fastapi import Request

from db.utils.database import databaseConnect, databaseDisconnect
from .services import (
    fetch_filtered_leave_type_info,
    fetch_filtered_leave_issuer_info,
    fetch_filtered_employee_leaves_info,
)


async def fetch_leave_type_info(request: Request, leave_type_id: str):
    conn = await databaseConnect()

    try:
        if leave_type_id:
            return await fetch_filtered_leave_type_info(conn, leave_type_id)
        return await fetch_filtered_leave_type_info(conn)
    finally:
        await databaseDisconnect(conn)


async def fetch_leave_issuer_info(request: Request, leave_issuer_id: str):
    conn = await databaseConnect()

    try:
        if leave_issuer_id:
            return await fetch_filtered_leave_issuer_info(conn, leave_issuer_id)
        return await fetch_filtered_leave_issuer_info(conn)
    finally:
        await databaseDisconnect(conn)


async def fetch_employee_leaves_info(
    request: Request,
    employee_id: str,
    leave_type_id: str,
    status: str,
    start_date: str,
    end_date: str,
    size: int,
):
    conn = await databaseConnect()

    try:
        if employee_id or leave_type_id or status or start_date or end_date or size:
            return await fetch_filtered_employee_leaves_info(
                conn, employee_id, leave_type_id, status, start_date, end_date, size
            )
        return await fetch_filtered_employee_leaves_info(conn)
    finally:
        await databaseDisconnect(conn)
