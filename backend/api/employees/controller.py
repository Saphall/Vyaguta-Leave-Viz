from fastapi import Request

from .services import fetch_filtered_employee_info
from db.utils.database import databaseConnect, databaseDisconnect


async def fetch_employee_info(
    request: Request,
    employee_id: int,
    designation_id: int,
    department_id: int,
    team_manager_id: int,
):
    conn = await databaseConnect()

    try:
        if employee_id or designation_id or department_id or team_manager_id:
            return await fetch_filtered_employee_info(
                conn, employee_id, designation_id, department_id, team_manager_id
            )
        return await fetch_filtered_employee_info(conn)
    finally:
        await databaseDisconnect(conn)
