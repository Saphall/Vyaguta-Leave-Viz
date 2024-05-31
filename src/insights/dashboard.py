# import time
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.insights import sql
from src.insights.utils.sql import fetch_data
from src.insights.page.leave_trend import leave_trend
from src.insights.page.employee import emp_visualization
from src.db.utils.database import databaseConnect, databaseDisconnect


st.set_page_config(
    page_title="Vyaguta Leave Viz", layout="wide", initial_sidebar_state="expanded"
)


# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Emp Visualization", "Leave Information"])

conn = databaseConnect()
if page == "Home":
    st.write("# :frog: Vyaguta Leave Visualization")
    st.write("---")
    st.write(
        "##### Welcome to the Vyaguta Leave Visualization tool. This tool allows you to explore leave data for employees, including leave types and leave days. Use the navigation on the left to view different visualizations and data."
    )
    st.html("<br>")
    st.image("https://vyaguta.lftechnology.com/api/auth/images/team-frog.svg")
    # All data
    sql = "SELECT * FROM raw.imported_leave_information"
    df = pd.read_sql(sql, conn)
    st.write("---")
    st.write(df)
    st.write("---")

elif page == "Leave Information":
    st.title("Leave Trends")
    all_data = leave_trend(conn)

    # Create a column for the selectbox
    col1, col2 = st.columns([1, 3])

    fiscal_id = col1.multiselect(
        "Select the Fiscal Date:",
        options=all_data["fiscal_date"].unique(),
        default=all_data["fiscal_date"].unique(),
    )

    department = col2.multiselect(
        "Select the department:",
        options=all_data["employee_department"].unique(),
        default=all_data["employee_department"].unique(),
    )

    designation = col2.multiselect(
        "Select the designation:",
        options=all_data["employee_designation"].unique(),
        default=all_data["employee_designation"].unique(),
    )

    leave_type = col1.multiselect(
        "Select the leave type:",
        options=all_data["leave_type"].unique(),
        default=all_data["leave_type"].unique(),
    )

    df_selection = all_data.query(
        "fiscal_date == @fiscal_id & employee_department ==@department & employee_designation == @designation & @leave_type== leave_type"
    )
    ####################### Month and Day wise Leave Trend################################

    monthly_leaves_columns = df_selection[["month_number", "month", "leave_days"]]
    group_monthly_leaves = monthly_leaves_columns.groupby(by=["month_number", "month"])[
        "leave_days"
    ].sum()
    unique_monthly_leaves = group_monthly_leaves.to_frame()
    # After performing the groupby operation
    unique_monthly_leaves.reset_index(inplace=True)

    # Selecting only 'month' and 'leave_days' columns
    final_monthly_leave_columns = unique_monthly_leaves[["month", "leave_days"]]

    # Leaves BY MOnth [BAR CHART]

    fig_monthly_sales = px.line(
        final_monthly_leave_columns,
        x=final_monthly_leave_columns["month"],
        y="leave_days",
        title="<b>Leaves by Month</b>",
        color_discrete_sequence=["#0083B8"] * len(final_monthly_leave_columns),
        template="plotly_white",
    )
    fig_monthly_sales.update_layout(
        xaxis=dict(tickmode="auto"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

    ###################### EMPLOYEE WISE LEAVE TREND ############################
    employee_leave_columns = df_selection.groupby(by=["employee_first_name"])[
        "leave_days"
    ].sum()

    # Leaves BY MOnth [BAR CHART]

    fig_employee_leaves = px.bar(
        employee_leave_columns,
        x=employee_leave_columns.index,
        y="leave_days",
        title="<b>Leaves by Employee</b>",
        color_discrete_sequence=["#0083B8"] * len(final_monthly_leave_columns),
        template="plotly_white",
    )
    fig_employee_leaves.update_layout(
        xaxis=dict(tickmode="auto"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

    st.plotly_chart(fig_monthly_sales, use_container_width=True)
    st.plotly_chart(fig_employee_leaves, use_container_width=True)

elif page == "Emp Visualization":
    st.title("Employee Visualization")
    df_grouped = emp_visualization(conn)
    # Create a column for the selectbox
    col1, col2 = st.columns([1, 3])

    # Create a selectbox for the employees in the first column
    selected_employee = col1.selectbox(
        "Select an employee", df_grouped["firstname"].unique(), key="employee_select"
    )

    # Filter the DataFrame for the selected employee
    df_filtered = df_grouped[df_grouped["firstname"] == selected_employee]

    # Drop the firstname column and transpose the DataFrame for plotting
    df_filtered = df_filtered.drop(columns="firstname").T.reset_index()
    df_filtered.columns = ["leavetypename", "leavedays"]

    # Create an interactive bar chart
    fig = px.bar(df_filtered, x="leavetypename", y="leavedays", text="leavedays")

    # Display the DataFrame in the second column
    col1.write(df_filtered)
    # Display the chart in the second column
    col2.plotly_chart(fig)

    ## ----
    ## ----
    data = fetch_data(f"{sql.__path__[0]}/employee_details.sql")
    alloc_data = fetch_data(f"{sql.__path__[0]}/allocation_details.sql")
    leave_data = fetch_data(f"{sql.__path__[0]}/leave_balance.sql")

    # Convert two columns of DataFrame into dictionary
    result_dict = dict(zip(data["full_name"], data["employee_id"]))

    # Select box
    selected_display_value = st.selectbox(
        "Select an option:", sorted(list(result_dict.keys()))
    )

    selected_associated_variable = result_dict.get(selected_display_value)

    emp_details = data.query("employee_id == @selected_associated_variable")
    alloc_details = alloc_data.query("employee_id == @selected_associated_variable")

    st.write(
        emp_details[
            ["first_name", "last_name", "email", "department_name", "designation_name"]
        ].style.set_table_attributes('style="width:100%"')
    )
    st.subheader("Allocation Details")
    st.write(
        alloc_details[["allocation_id", "name", "type"]].style.set_table_attributes(
            'style="width:500%"'
        )
    )

    st.subheader("Leave Balance")
    fiscal_id = st.selectbox(
        "Select the Fiscal Date:", options=leave_data["fiscal_date"].unique()
    )

    # Define the number of columns you want (4x2 matrix)
    num_columns = 2
    num_rows = 4

    # Initialize Streamlit columns
    columns = [st.columns(num_columns) for _ in range(num_rows)]

    # Counter to keep track of figures
    figure_counter = 0

    leave_details = leave_data.query(
        "employee_id == @selected_associated_variable & fiscal_date == @fiscal_id"
    )

    for index, row in leave_details.iterrows():
        value = row["total"]
        # Create the gauge chart
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                title={
                    "text": row["leave_type"] + " Default: " + str(row["default_days"])
                },
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={"axis": {"range": [None, row["default_days"]]}},
            )
        )

        # Update the layout to remove axis ticks and labels
        fig.update_layout(
            xaxis={"showticklabels": False}, yaxis={"showticklabels": False}
        )

        # Show the chart in the appropriate column and row
        columns[figure_counter // num_columns][
            figure_counter % num_columns
        ].plotly_chart(fig, use_container_width=True, height=100)
    figure_counter += 1


databaseDisconnect(conn)


def reload():
    pass
