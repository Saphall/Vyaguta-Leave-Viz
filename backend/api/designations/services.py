from backend.utils.util import convert_list_to_dict


async def fetch_filtered_designations_info(
    conn,
    designation_id=None,
):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.dim_designations"
        params = []
        conditions = []

        if designation_id:
            conditions.append("CAST(designation_id AS INT) = %s")
            params.append(designation_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        departments_data_dict = convert_list_to_dict(cur)
        departments_data_dict.append({"total_count": len(departments_data_dict)})

        return {"data": departments_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}
