import streamlit as st
import plotly.express as px

from src.insights import sql
from src.insights.utils.sql import fetch_data


def main(conn):
    st.title("Leave Trends")
    all_data = fetch_data(f"{sql.__path__[0]}/employee_all_leave_data.sql")

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
