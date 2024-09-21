async def fetch_filtered_all_leave_info(
    conn, designationID=None, startDate=None, endDate=None, size=None
):
    try:
        cur = conn.cursor()
        query = """
            SELECT * FROM raw.imported_leave_information
        """
        params = []
        conditions = []

        if startDate:
            conditions.append("CAST(startdate AS DATE) >= %s")
            params.append(startDate)

        if endDate:
            conditions.append("CAST(enddate AS DATE) <= %s")
            params.append(endDate)

        if designationID:
            conditions.append("CAST(designationid AS INT) = %s")
            params.append(designationID)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if size:
            query += " LIMIT %s"
            params.append(size)

        cur.execute(query, params)
        leave_data = cur.fetchall()

        # Convert the list of tuples to a list of dictionaries
        columns = [desc[0] for desc in cur.description]
        leave_data_dict = [dict(zip(columns, row)) for row in leave_data]
        leave_data_dict.append({"total_leave_count": len(leave_data_dict)})

        return {"data": leave_data_dict, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Invalid Arguments provided in request.", "status_code": 404}
