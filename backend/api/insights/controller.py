from fastapi import Request
from typing import List

from .services import (
    fetch_filtered_employee_details_insight,
    fetch_filtered_employee_leaves_insight,
    fetch_filtered_leave_balance_insight,
)
from db.utils.database import databaseConnect, databaseDisconnect


async def fetch_employee_details_insight(
    request: Request,
    employee_name: List[str],
    fiscal_year: List[str],
    start_date: str,
    end_date: str,
    size: int,
):
    conn = await databaseConnect()
    try:
        if employee_name or fiscal_year or start_date or end_date or size:
            return await fetch_filtered_employee_details_insight(
                conn, employee_name, fiscal_year, start_date, end_date, size
            )
        return await fetch_filtered_employee_details_insight(conn)

    finally:
        await databaseDisconnect(conn)


async def fetch_employee_leaves_insight(
    request: Request,
    employee_name: List[str],
    fiscal_year: List[str],
    designation_name: List[str],
    department_name: List[str],
    leave_type: List[str],
    status: List[str],
    start_date: str,
    end_date: str,
    size: int,
):
    conn = await databaseConnect()

    try:
        if (
            employee_name
            or fiscal_year
            or designation_name
            or department_name
            or leave_type
            or status
            or start_date
            or end_date
            or size
        ):
            return await fetch_filtered_employee_leaves_insight(
                conn,
                employee_name,
                fiscal_year,
                designation_name,
                department_name,
                leave_type,
                status,
                start_date,
                end_date,
                size,
            )
        return await fetch_filtered_employee_leaves_insight(conn)
    finally:
        await databaseDisconnect(conn)


async def fetch_leave_balance_insight(
    request: Request,
    employee_name: List[str],
    leave_type: List[str],
    fiscal_year: List[str],
    start_date: str,
    end_date: str,
    size: int,
):
    conn = await databaseConnect()
    try:
        if employee_name or leave_type or fiscal_year or start_date or end_date or size:
            return await fetch_filtered_leave_balance_insight(
                conn, employee_name, leave_type, fiscal_year, start_date, end_date, size
            )
        return await fetch_filtered_leave_balance_insight(conn)

    finally:
        await databaseDisconnect(conn)
