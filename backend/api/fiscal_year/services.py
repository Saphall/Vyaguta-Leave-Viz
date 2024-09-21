from backend.utils.util import convert_list_to_dict


async def fetch_filtered_fiscal_year_info(
    conn,
    fiscal_id=None,
    start_date=None,
    end_date=None,
):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM dbo.fiscal_year"
        params = []
        conditions = []

        if fiscal_id:
            conditions.append("CAST(fiscal_id AS INT) = %s")
            params.append(fiscal_id)
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
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        fiscal_year_data_dict = convert_list_to_dict(cur)
        fiscal_year_data_dict.append({"total_count": len(fiscal_year_data_dict)})

        return {"data": fiscal_year_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}
