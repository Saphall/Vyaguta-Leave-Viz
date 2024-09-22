from datetime import datetime
import db
import json
import httpx

from backend.utils.constants import VYAGUTA_URL
from backend.utils.sql import LEAVE_DATA_INSERT_QUERY


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
    try:
        cur = conn.cursor()
        raw_leave_table = "raw.imported_leave_information"

        cur.execute(f"TRUNCATE TABLE {raw_leave_table}")
        query = LEAVE_DATA_INSERT_QUERY.format(raw_table_name=raw_leave_table)

        for row in data:
            if row["allocations"] is not None:
                row["allocations"] = json.dumps(row["allocations"])
            cur.execute(query, row)
            conn.commit()

        print("\n[INFO]: Leave Data Imported Successfully! Starting ETL ...")

        with open(f"{db.__path__[0]}/procedures.json", encoding="utf-8") as f:
            etl_steps = json.load(f)

        for step in etl_steps["extract"]:
            cur.execute(f'CALL {step["proc"]}();')
            conn.commit()
        print("\n\t[INFO]: Leave Data Extracted Successfully!")

        for step in etl_steps["transform"]:
            cur.execute(f'CALL {step["proc"]}();')
            conn.commit()
        print("\t[INFO]: Leave Data Transformed Successfully!")

        for step in etl_steps["load"]:
            cur.execute(f'CALL {step["proc"]}();')
            conn.commit()
        print("\t[INFO]: Leave Data Loaded Successfully!")

        print("\n[SUCCESS]: ETL process Completed!\n")
        return {"success": "Leave Data Inserted Successfully!", "status_code": 200}
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return {"error": str(e), "status_code": 404}
