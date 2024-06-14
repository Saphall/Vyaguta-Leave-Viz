import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.insights import sql
from src.insights.utils.sql import fetch_data


def emp_visualization(conn):
    query = "SELECT empid, firstname, leavetypename, leavedays FROM raw.imported_leave_information;"
    df = pd.read_sql_query(query, conn)
    df["leavedays"] = pd.to_numeric(df["leavedays"], errors="coerce")
    df_grouped = (
        df.groupby(["firstname", "leavetypename"])["leavedays"]
        .sum()
        .unstack()
        .reset_index()
        .fillna(0)
    )
    return df_grouped


def create_card(employee):
    card_html = f"""
    <div style='
        background-color: #333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        width: 100%;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5);
        color: #fff;
        font-family: Arial, sans-serif;
    '>
        <h4 style='margin-bottom: 8px; color: #ffcc00;'>{employee["first_name"]} {employee["last_name"]}</h4>
        <p style='margin-bottom: 4px;'><b>Email:</b> {employee["email"]}</p>
        <p style='margin-bottom: 4px;'><b>Department:</b> {employee["department_name"]}</p>
        <p style='margin-bottom: 0;'><b>Designation:</b> {employee["designation_name"]}</p>
    </div>
    """
    return card_html


def main(conn):
    st.title("Employee Visualization")
    df_grouped = emp_visualization(conn)

    # Fetch additional data
    data = fetch_data(f"{sql.__path__[0]}/employee_details.sql")
    alloc_data = fetch_data(f"{sql.__path__[0]}/allocation_details.sql")
    leave_bal = fetch_data(f"{sql.__path__[0]}/leave_balance.sql")

    result_dict = dict(zip(data["full_name"], data["employee_id"]))

    # Row 1: Select box
    with st.container():
        selected_display_value = st.selectbox(
            "Select an employee:", sorted(list(result_dict.keys()))
        )
        selected_associated_variable = result_dict.get(selected_display_value)

    # Fetch details for selected employee
    emp_details = data.query("employee_id == @selected_associated_variable")
    alloc_details = alloc_data.query("employee_id == @selected_associated_variable")

    # Row 2: Employee Card
    with st.container():
        for index, row in emp_details.iterrows():
            card_html = create_card(row)
            st.markdown(card_html, unsafe_allow_html=True)

    # Row 3: Allocation Details
    with st.container():
        st.subheader("Allocation Details")
        st.write(
            alloc_details[["allocation_id", "name", "type"]].style.set_table_attributes(
                'style="width:100%"'
            )
        )

    # Filter data for the selected employee
    df_filtered = df_grouped[
        df_grouped["firstname"] == str(selected_display_value).split(" ")[0]
    ]
    df_filtered = df_filtered.drop(columns="firstname").T.reset_index()
    df_filtered.columns = ["leavetypename", "leavedays"]

    # Create bar chart for leave details
    fig = px.bar(df_filtered, x="leavetypename", y="leavedays", text="leavedays")

    # Row 4: Leave Details with Two Columns
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Leave Details")
            st.write(df_filtered)
        with col2:
            st.plotly_chart(fig)

    # Row 5: Leave Balance
    with st.container():
        st.subheader("Leave Balance")

        # Get unique fiscal dates and determine the index of the default option
        fiscal_dates = leave_bal["fiscal_date"].unique()
        default_fiscal = "2023/2024"
        if default_fiscal in fiscal_dates:
            default_index = list(fiscal_dates).index(default_fiscal)
        else:
            default_index = 0  # Fallback to the first option if not found

        fiscal_id = st.selectbox(
            "Select the Fiscal Date:", options=fiscal_dates, index=default_index
        )

        # Define the number of columns and rows
        num_columns = 2
        num_rows = 4
        max_charts = num_columns * num_rows  # Total number of slots for charts

        # Initialize columns list to hold columns
        columns = [st.columns(num_columns) for _ in range(num_rows)]

        leave_details = leave_bal.query(
            "employee_id == @selected_associated_variable & fiscal_date == @fiscal_id"
        )

        figure_counter = 0
        for index, row in leave_details.iterrows():
            if figure_counter >= max_charts:
                st.warning("Maximum number of charts exceeded!")
                break

            value = row["total"]
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=value,
                    title={
                        "text": f'{row["leave_type"]} Default: {row["default_days"]}'
                    },
                    domain={"x": [0, 1], "y": [0, 1]},
                    gauge={"axis": {"range": [None, row["default_days"]]}},
                )
            )
            fig.update_layout(
                xaxis={"showticklabels": False}, yaxis={"showticklabels": False}
            )

            row_index = figure_counter // num_columns
            col_index = figure_counter % num_columns

            # Ensure row_index and col_index are within bounds
            if row_index < num_rows and col_index < num_columns:
                columns[row_index][col_index].plotly_chart(
                    fig, use_container_width=True, height=100
                )
                figure_counter += 1
