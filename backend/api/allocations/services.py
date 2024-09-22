from backend.utils.util import convert_list_to_dict


async def fetch_filtered_allocations_info(
    conn,
    allocation_id=None,
):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.dim_allocations"
        params = []
        conditions = []

        if allocation_id:
            conditions.append("CAST(allocation_id AS INT) = %s")
            params.append(allocation_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        allocations_data_dict = convert_list_to_dict(cur)
        allocations_data_dict.append({"total_count": len(allocations_data_dict)})

        return {"data": allocations_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}
