from backend.utils.util import convert_list_to_dict


async def fetch_filtered_employee_info(
    conn,
    employee_id=None,
    designation_id=None,
    department_id=None,
    team_manager_id=None,
):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.employees"
        params = []
        conditions = []

        if employee_id:
            conditions.append("CAST(employee_id AS INT) = %s")
            params.append(employee_id)
        if designation_id:
            conditions.append("CAST(designation_id AS INT) = %s")
            params.append(designation_id)
        if department_id:
            conditions.append("CAST(department_id AS INT) = %s")
            params.append(department_id)
        if team_manager_id:
            conditions.append("CAST(team_manager_id AS INT) = %s")
            params.append(team_manager_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        employee_data_dict = convert_list_to_dict(cur)
        employee_data_dict.append({"total_count": len(employee_data_dict)})

        return {"data": employee_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}
