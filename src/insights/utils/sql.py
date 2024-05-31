import pandas as pd
from src.db.utils.database import databaseConnect, databaseDisconnect


def fetch_data(sql_file):
    try:
        # Open and read the SQL file with specified encoding
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_queries = file.read()

        # Connect to the database and fetch data
        conn = databaseConnect()
        all_data = pd.read_sql(sql_queries, conn)
        databaseDisconnect(conn)
        return all_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
