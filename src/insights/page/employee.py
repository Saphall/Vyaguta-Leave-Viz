import pandas as pd


def emp_visualization(conn):
    # Query the data
    query = "SELECT firstname, leavetypename, leavedays FROM raw.imported_leave_information;"
    df = pd.read_sql_query(query, conn)
    # Convert leavedays to numeric
    df["leavedays"] = pd.to_numeric(df["leavedays"], errors="coerce")

    # Group by employee and leave type, and sum the leave days
    df_grouped = (
        df.groupby(["firstname", "leavetypename"])["leavedays"]
        .sum()
        .unstack()
        .reset_index()
        .fillna(0)
    )

    return df_grouped
