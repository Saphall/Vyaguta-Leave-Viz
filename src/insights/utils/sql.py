import pandas as pd
from src.db.utils.database import databaseConnect, databaseDisconnect


async def fetch_data(sql_file):
    try:
        # Open and read the SQL file with specified encoding
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_queries = file.read()

        # Connect to the database and fetch data
        conn = await databaseConnect()
        all_data = pd.read_sql(sql_queries, conn)
        await databaseDisconnect(conn)
        return all_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
