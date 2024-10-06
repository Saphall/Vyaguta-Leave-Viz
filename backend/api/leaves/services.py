from backend.utils.util import convert_list_to_dict


async def fetch_filtered_leave_type_info(conn, leave_type_id=None):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.dim_leave_types"
        params = []
        conditions = []

        if leave_type_id:
            conditions.append("CAST(leave_type_id AS INT) = %s")
            params.append(leave_type_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        leave_types_dict = convert_list_to_dict(cur)
        leave_types_dict.append({"total_count": len(leave_types_dict)})

        return {"data": leave_types_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}


async def fetch_filtered_leave_issuer_info(conn, leave_issuer_id=None):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.dim_leave_issuer"
        params = []
        conditions = []

        if leave_issuer_id:
            conditions.append("CAST(leave_issuer_id AS INT) = %s")
            params.append(leave_issuer_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        leave_issuers_dict = convert_list_to_dict(cur)
        leave_issuers_dict.append({"total_count": len(leave_issuers_dict)})

        return {"data": leave_issuers_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}


async def fetch_filtered_employee_leaves_info(
    conn,
    employee_id=None,
    leave_type_id=None,
    status=None,
    start_date=None,
    end_date=None,
    size=None,
):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.fact_employee_leaves"
        params = []
        conditions = []

        if employee_id:
            conditions.append("CAST(employee_id AS INT) = %s")
            params.append(employee_id)
        if leave_type_id:
            conditions.append("CAST(leave_type_id AS INT) = %s")
            params.append(leave_type_id)
        if status:
            conditions.append("CAST(status AS VARCHAR) = %s")
            params.append(status)
        if start_date and end_date:
            conditions.append(
                "CAST(start_date AS DATE) >= %s AND CAST(end_date AS DATE) <= %s"
            )
            params.append(start_date)
            params.append(end_date)
        elif start_date:
            conditions.append("CAST(start_date AS DATE) >= %s")
            params.append(start_date)
        elif end_date:
            conditions.append("CAST(end_date AS DATE) <= %s")
            params.append(end_date)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        if size:
            query += " LIMIT %s"
            params.append(size)

        cur.execute(query, params)
        employee_leaves_dict = convert_list_to_dict(cur)
        employee_leaves_dict.append({"total_count": len(employee_leaves_dict)})

        return {"data": employee_leaves_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}
