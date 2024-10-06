from backend.utils.util import convert_list_to_dict


async def fetch_filtered_employee_details_insight(
    conn,
    employee_name=None,
    fiscal_year=None,
    start_date=None,
    end_date=None,
    size=None,
):
    try:

        cur = conn.cursor()
        query = "SELECT * FROM dbo.vw_employee_details_insight"
        params = []
        conditions = []

        if employee_name:
            conditions.append("employee_name = ANY(%s)")
            params.append(employee_name)
        if fiscal_year:
            conditions.append("fiscal_date = ANY(%s)")
            params.append(fiscal_year)
        if start_date:
            conditions.append("CAST(start_date AS DATE) >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("CAST(end_date AS DATE) <= %s")
            params.append(end_date)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        if size:
            query += " LIMIT %s"
            params.append(size)

        cur.execute(query, params)
        employee_data_dict = convert_list_to_dict(cur)
        employee_data_dict.append({"total_count": len(employee_data_dict)})

        return {"data": employee_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {
            "error": "Invalid Arguments provided.",
            "status_code": 404,
        }


async def fetch_filtered_employee_leaves_insight(
    conn,
    employee_name=None,
    fiscal_year=None,
    designation_name=None,
    department_name=None,
    leave_type=None,
    status=None,
    start_date=None,
    end_date=None,
    size=None,
):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.vw_employee_leaves_insight"
        params = []
        conditions = []

        if employee_name:
            conditions.append("employee_name = ANY(%s)")
            params.append(employee_name)
        if fiscal_year:
            conditions.append("fiscal_date = ANY(%s)")
            params.append(fiscal_year)
        if designation_name:
            conditions.append("employee_designation = ANY(%s)")
            params.append(designation_name)
        if department_name:
            conditions.append("employee_department = ANY(%s)")
            params.append(department_name)
        if leave_type:
            conditions.append("leave_type = ANY(%s)")
            params.append(leave_type)
        if status:
            conditions.append("status = ANY(%s)")
            params.append(status)
        if start_date:
            conditions.append("CAST(start_date AS DATE) >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("CAST(end_date AS DATE) <= %s")
            params.append(end_date)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        if size:
            query += " LIMIT %s"
            params.append(size)

        cur.execute(query, params)
        employee_data_dict = convert_list_to_dict(cur)
        employee_data_dict.append({"total_count": len(employee_data_dict)})

        return {"data": employee_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {
            "error": "Invalid Arguments provided.",
            "status_code": 404,
        }


async def fetch_filtered_leave_balance_insight(
    conn,
    employee_name=None,
    leave_type=None,
    fiscal_year=None,
    start_date=None,
    end_date=None,
    size=None,
):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.vw_leave_balance_insight"
        params = []
        conditions = []

        if employee_name:
            conditions.append("employee_name = ANY(%s)")
            params.append(employee_name)
        if leave_type:
            conditions.append("leave_type = ANY(%s)")
            params.append(leave_type)
        if fiscal_year:
            conditions.append("fiscal_date = ANY(%s)")
            params.append(fiscal_year)
        if start_date:
            conditions.append("CAST(start_date AS DATE) >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("CAST(end_date AS DATE) <= %s")
            params.append(end_date)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        if size:
            query += " LIMIT %s"
            params.append(size)

        cur.execute(query, params)
        employee_data_dict = convert_list_to_dict(cur)
        employee_data_dict.append({"total_count": len(employee_data_dict)})

        return {"data": employee_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {
            "error": "Invalid Arguments provided.",
            "status_code": 404,
        }
