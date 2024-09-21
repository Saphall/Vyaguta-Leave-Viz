from datetime import datetime
import json
import httpx
from src import db
from src.backend.utils.constants import VYAGUTA_URL


async def get_leave_info(bearer_token: str):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                VYAGUTA_URL.format(current_date=datetime.now().date()),
                headers=headers,
                timeout=1000,
            )
            return response

    except httpx.RequestError:
        return {"error": "Internal Server Error", "status_code": 500}


async def insert_leave_info(data, conn):
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE raw.imported_leave_information")
    query = """
        INSERT INTO raw.imported_leave_information(
            id, userId, empId, teamManagerId, designationId, designationName, firstName, middleName, lastName, email, 
            isHr, isSupervisor, allocations, leaveIssuerId, currentLeaveIssuerId, issuerFirstName, issuerMiddleName, issuerLastName, 
            currentLeaveIssuerEmail, departmentDescription, startDate, endDate, leaveDays, reason, leaveStatus, status, responseRemarks, leaveTypeId, 
            leaveType, defaultDays, transferableDays, isConsecutive, fiscalId, fiscalStartDate, fiscalEndDate, fiscalIsCurrent, 
            createdAt, updatedAt, isAutomated, isConverted, totalCount
        ) VALUES (
            %(id)s, %(userId)s, %(empId)s, %(teamManagerId)s, %(designationId)s, %(designationName)s, %(firstName)s, %(middleName)s, 
            %(lastName)s, %(email)s, %(isHr)s, %(isSupervisor)s, %(allocations)s, %(leaveIssuerId)s, %(currentLeaveIssuerId)s, 
            %(issuerFirstName)s, %(issuerMiddleName)s, %(issuerLastName)s, %(currentLeaveIssuerEmail)s, %(departmentDescription)s, %(startDate)s, 
            %(endDate)s, %(leaveDays)s, %(reason)s, %(leaveStatus)s, %(status)s, %(responseRemarks)s, %(leaveTypeId)s, %(leaveType)s, %(defaultDays)s, 
            %(transferableDays)s, %(isConsecutive)s, %(fiscalId)s, %(fiscalStartDate)s, %(fiscalEndDate)s, %(fiscalIsCurrent)s, 
            %(createdAt)s, %(updatedAt)s, %(isAutomated)s, %(isConverted)s, %(totalCount)s
        )
        """
    for row in data:
        if row["allocations"] is not None:
            row["allocations"] = json.dumps(row["allocations"])
        cur.execute(query, row)
        conn.commit()

    with open(f"{db.__path__[0]}/procedures.json", encoding="utf-8") as f:
        proc_steps = json.load(f)
    for step in proc_steps["steps"]:
        cur.execute(f'CALL {step["proc"]}();')
        conn.commit()
