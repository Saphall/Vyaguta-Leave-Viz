import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from collections import Counter, defaultdict
from insights.utils.designs import create_card
from insights.utils.api import leave_types_data, get_api_data
from insights.utils.constants import EMPLOYEE_LEAVES_INSIGHT_URL
from st_aggrid import AgGrid, GridOptionsBuilder
from insights.utils.filters import (
    fiscal_year_filter_values,
    department_filter_values,
    leave_types_filter_values,
    designation_filter_values,
    min_start_date,
)

st.caption(":material/tune: Filters")
col1, col2, col3, col4, col5 = st.columns([0.4, 0.4, 0.4, 0.4, 1])

# ===== Filter: leave_types
leave_type_popover = col1.popover(
    ":material/filter_alt: Leave Type", help="Leave Type filter for visualization"
)
selected_leave_types = leave_type_popover.multiselect(
    ":palm_tree: Leave Types",
    leave_types_filter_values,
    # default=leave_types_filter_values,
)

# ===== Filter: deparments
deparment_popover = col2.popover(
    ":material/filter_alt: Department", help="Department filter for visualization"
)
selected_departments = deparment_popover.multiselect(
    ":office: Departments",
    department_filter_values,
    # default=department_filter_values
)

# ===== Filter: designations
designationn_popover = col3.popover(
    ":material/filter_alt: Designation", help="Designation filter for visualization"
)
selected_designations = designationn_popover.multiselect(
    ":male-technologist: Designations",
    designation_filter_values,
    # default=designation_filter_values,
)

# ===== Filter: fiscal_year
fiscal_year_popover = col4.popover(
    ":material/filter_alt: Fiscal Year", help="Fiscal Year filter for visualization"
)
selected_fiscal_years = fiscal_year_popover.multiselect(
    ":date: Fiscal Years",
    fiscal_year_filter_values,
    # default=fiscal_year_filter_values
)


# ==== Filter: start_date
start_date = min_start_date.replace(month=1, day=1)
current_date = datetime.datetime.now().date()
end_of_year_date = current_date.replace(month=12, day=31)

selected_start_date_range = col5.slider(
    "Date Range:",
    min_value=start_date,
    max_value=end_of_year_date,
    value=(min_start_date, current_date),
    format="YYYY-MM-DD",
    help="Select the date range for the leave data",
)
selected_start_date, selected_end_date = selected_start_date_range
st.divider()


## ==============Fetch Insights Data=================
query_params = {}
if selected_fiscal_years:
    query_params["fiscal_date"] = selected_fiscal_years
if selected_departments:
    query_params["department_name"] = selected_departments
if selected_leave_types:
    query_params["leave_type"] = selected_leave_types
if selected_designations:
    query_params["designation_name"] = selected_designations
if selected_start_date and selected_end_date:
    query_params["start_date"] = selected_start_date
    query_params["end_date"] = selected_end_date
# Employee Leaves Insights Data
employee_leaves_insight_data = get_api_data(
    EMPLOYEE_LEAVES_INSIGHT_URL, query=query_params
)

st.caption("KPIs")
col1, col2, col3, col4 = st.columns([1, 0.6, 0.5, 0.5])


## ==============Visualizations=====================
# =============== Top Leave Taking Employees =======
employee_leave_days = defaultdict(int)
for entry in employee_leaves_insight_data["data"]:
    if (
        "employee_name" in entry
        and "leave_days" in entry
        and entry["status"] in ["APPROVED"]
    ):
        employee_leave_days[entry["employee_name"]] += entry["leave_days"]
# Sort employees by total leave days in descending order
sorted_employees = sorted(employee_leave_days.items(), key=lambda x: x[1], reverse=True)
top_leave_taking_employees = sorted_employees[:5]

# Create a DataFrame for the top leave-taking employees
df_top_employees = pd.DataFrame(
    top_leave_taking_employees, columns=["Employee Name", "Leave Days"]
)
fig = px.bar(
    df_top_employees,
    x="Leave Days",
    y="Employee Name",
    orientation="h",
    title="Top Leave Taking Employees",
    text="Leave Days",
    height=350,
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
with col1:
    st.plotly_chart(fig, use_container_width=True)


# =============== Most Used Leave Type ===========
# Extract leave types from the data
leave_types = [
    entry["leave_type"]
    for entry in employee_leaves_insight_data["data"]
    if "leave_type" in entry
]
# Count the occurrences of each leave type
leave_type_counts = Counter(leave_types)
# Determine the most used leave type
if leave_type_counts:
    most_used_leave_type = leave_type_counts.most_common(1)[0][0]
else:
    most_used_leave_type = "Data Not available"

with col2:
    st.caption("")
    st.caption("")
    st.markdown(
        create_card(
            title="Most Used Leave",
            value=most_used_leave_type,
        ),
        unsafe_allow_html=True,
    )


# =============== Average Number of Leave Days ===========
# Extract leave days from the data
leave_days = [
    entry["leave_days"]
    for entry in employee_leaves_insight_data["data"]
    if "leave_days" in entry and entry["status"] == "APPROVED"
]
# leave_days.sort()
total_employees_on_leave = len(
    set(
        entry["employee_name"]
        for entry in employee_leaves_insight_data["data"]
        if "employee_name" in entry and entry["status"] == "APPROVED"
    )
)

#  Calculate the average number of leave days
if leave_days:
    average_leave_days = sum(leave_days) / total_employees_on_leave
    if total_employees_on_leave > 2:
        sorted_leave_days = sorted(leave_days)
        trimmed_mean = np.mean(sorted_leave_days[1:-1])
    else:
        trimmed_mean = average_leave_days
else:
    average_leave_days = 0
    trimmed_mean = 0

with col3:
    st.caption("")
    st.caption("")
    st.markdown(
        create_card(
            title="Average Leave Days",
            value=f"{trimmed_mean:.2f} Days",
        ),
        unsafe_allow_html=True,
    )


# =============== Default Leave Days ===========
#  Calculate total default days
sick_leave = next(item for item in leave_types_data if item["leave_type"] == "Sick")
discretionary = next(
    item for item in leave_types_data if item["leave_type"] == "Discretionary"
)
total_default_days = sick_leave["default_days"] + discretionary["default_days"]

with col4:
    st.caption("")
    st.caption("")
    st.markdown(
        create_card(title="Default Leave Days", value=f"{total_default_days} Days"),
        unsafe_allow_html=True,
    )
    st.info(
        f"- Sick Leave: {sick_leave['default_days']} Days\n - Discretionary: {discretionary['default_days']} Days"
    )


# =============== Leave Issuer and  Request ===========
col1, col2, col3 = st.columns([1, 0.4, 0.3])
# Aggregate leave requests by issuer
leave_issuers = [
    f"{entry['leave_issuer_first_name']} {entry['leave_issuer_last_name']}"
    for entry in employee_leaves_insight_data["data"]
    if "leave_issuer_first_name" in entry
    and "leave_issuer_last_name" in entry
    and entry["leave_issuer_first_name"] is not None
    and entry["leave_issuer_last_name"] is not None
    and entry["status"] in ["APPROVED"]
]
leave_issuer_counts = Counter(leave_issuers)
top_leave_issuers = leave_issuer_counts.most_common(5)
df_top_leave_issuers = pd.DataFrame(
    top_leave_issuers, columns=["Leave Issuer", "Approved Leave Requests"]
)

fig = px.bar(
    df_top_leave_issuers,
    x="Approved Leave Requests",
    y="Leave Issuer",
    orientation="h",
    title="Top Leave Approvers",
    text="Approved Leave Requests",
    height=350,
    color="Approved Leave Requests",
    color_continuous_scale="Blues",
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
col1.plotly_chart(fig, use_container_width=True)


# ============= Total Employees on Leave ==========
total_employees_on_leave = len(
    set(
        entry["employee_name"]
        for entry in employee_leaves_insight_data["data"]
        if "employee_name" in entry and entry["status"] == "APPROVED"
    )
)
with col2:
    st.caption("")
    st.caption("")
    st.markdown(
        create_card(
            title="Total Employees on Leave",
            value=total_employees_on_leave,
        ),
        unsafe_allow_html=True,
    )


# ============= List of Employees on Leave ==========
employees_on_leave = sorted(
    set(
        entry["employee_name"]
        for entry in employee_leaves_insight_data["data"]
        if "employee_name" in entry and entry["status"] == "APPROVED"
    )
)
df_employees_on_leave = pd.DataFrame(employees_on_leave, columns=["Employee Name"])
with col3:
    st.caption("")
    st.caption("Employees on Leave")
    gb = GridOptionsBuilder.from_dataframe(df_employees_on_leave)
    gridOptions = gb.build()
    AgGrid(
        df_employees_on_leave,
        gridOptions=gridOptions,
        height=200,
        fit_columns_on_grid_load=True,
    )


# ==============================================
# =============== Leave Distribution ===========
st.divider()
st.markdown("<br>", unsafe_allow_html=True)
st.caption("Leave Info")
col1, col2 = st.columns([1, 0.8])

# ====== Total Leave by Leave Type =========
# Aggregate leave days by leave type
leave_days_by_type = defaultdict(int)
for entry in employee_leaves_insight_data["data"]:
    if (
        "leave_type" in entry
        and "leave_days" in entry
        and entry["status"] in ["APPROVED"]
    ):
        leave_days_by_type[entry["leave_type"]] += entry["leave_days"]

# Create a DataFrame for the leave distribution
df_leave_distribution = pd.DataFrame(
    list(leave_days_by_type.items()), columns=["Leave Type", "Total Leave Days"]
)

# Calculate the percentage of total leave days for each leave type
total_leave_days = df_leave_distribution["Total Leave Days"].sum()
df_leave_distribution["Percentage"] = (
    df_leave_distribution["Total Leave Days"] / total_leave_days
) * 100

with col1:
    fig = px.pie(
        df_leave_distribution,
        names="Leave Type",
        values="Total Leave Days",
        title="Leave Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(legend=dict(x=-0.1, y=0.5))

    st.plotly_chart(fig, use_container_width=True)


# ====== Total leave by Leave Status =========
# Aggregate leave days by leave status
leave_days_by_status = defaultdict(int)
for entry in employee_leaves_insight_data["data"]:
    if "status" in entry and "leave_days" in entry:
        leave_days_by_status[entry["status"]] += entry["leave_days"]

# Create a DataFrame for the leave status distribution
df_leave_status = pd.DataFrame(
    list(leave_days_by_status.items()), columns=["Leave Status", "Total Leave Days"]
)
df_leave_status = df_leave_status.sort_values(by="Total Leave Days", ascending=False)

with col2:
    # Define custom colors for specific leave statuses
    custom_colors = {
        "APPROVED": "green",
        "REQUESTED": "lightgreen",
        "CANCELLED": "lightcoral",
        "REJECTED": "lightcoral",
    }

    # Apply custom colors to the DataFrame
    df_leave_status["Color"] = df_leave_status["Leave Status"].apply(
        lambda status: custom_colors.get(status, px.colors.qualitative.Plotly[0])
    )

    fig = px.bar(
        df_leave_status,
        x="Leave Status",
        y="Total Leave Days",
        title="Leave Status Distribution",
        text="Total Leave Days",
        color="Color",
        color_discrete_map="identity",
    )
    fig.update_layout(xaxis_title="Leave Status", yaxis_title="Total Leave Days")
    st.plotly_chart(fig, use_container_width=True)


# ====== Leave Distribution by Department =========
st.divider()
st.caption("Department Info")

# ======== Total employees on leave per department
leave_records = (
    pd.DataFrame(employee_leaves_insight_data["data"])
    if employee_leaves_insight_data["data"]
    else pd.DataFrame()
)
if "status" in leave_records.columns:
    approved_leaves = leave_records[leave_records["status"] == "APPROVED"]

    employees_on_leave_per_department = (
        approved_leaves.groupby("employee_department")["employee_id"]
        .nunique()
        .reset_index()
    )
    employees_on_leave_per_department.columns = [
        "Department",
        "Total Employees on Leave",
    ]

    fig = px.area(
        employees_on_leave_per_department,
        x="Department",
        y="Total Employees on Leave",
        title="Employees on Leave per Department",
        line_shape="spline",
        markers=True,
        text="Total Employees on Leave",
        color_discrete_sequence=["#FFFFE0"],
    )
    fig.update_traces(
        text=employees_on_leave_per_department["Total Employees on Leave"],
        textposition="top right",
    )
    fig.update_layout(
        xaxis_title="Department Names",
        yaxis_title="Total Employees on Leave",
        yaxis=dict(
            range=[
                -10,
                employees_on_leave_per_department["Total Employees on Leave"].max()
                + 10,
            ]
        ),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.empty()


# ======= Total leaves per department
def new_func(employee_leaves_insight_data):
    leave_days_by_department = defaultdict(int)
    for record in employee_leaves_insight_data["data"]:
        if "employee_department" in record and record["status"] in ["APPROVED"]:
            department = record["employee_department"]
            leave_days_by_department[department] += record["leave_days"]

    # Create a DataFrame for the leave distribution by department
    df_leave_distribution = pd.DataFrame(
        list(leave_days_by_department.items()),
        columns=["Department", "Total Leave Days"],
    )

    # Calculate the sum of leave days for each department
    df_leave_distribution["Total Leave Days"] = df_leave_distribution[
        "Total Leave Days"
    ].astype(int)

    # Sort the DataFrame by Department
    df_leave_distribution = df_leave_distribution.sort_values(by="Department")

    fig = px.histogram(
        df_leave_distribution,
        x="Department",
        y="Total Leave Days",
        title="Total Leave Days by Department",
        text_auto=True,
        nbins=len(df_leave_distribution),
    )
    fig.update_layout(xaxis_title="Department Names", yaxis_title="Leave Days")
    st.plotly_chart(fig, use_container_width=True)


new_func(employee_leaves_insight_data)


# ======== Leave Distribution by Designation ==========
st.divider()
st.caption("Designation Info")

# ======== Total employees on leave per designation
if "status" in leave_records.columns:
    employees_on_leave_per_designation = (
        approved_leaves.groupby("employee_designation")["employee_id"]
        .nunique()
        .reset_index()
    )
    employees_on_leave_per_designation.columns = [
        "Designation",
        "Total Employees on Leave",
    ]

    fig = px.area(
        employees_on_leave_per_designation,
        x="Designation",
        y="Total Employees on Leave",
        title="Employees on Leave per Designation",
        line_shape="spline",
        markers=True,
        text="Total Employees on Leave",
        color_discrete_sequence=["lightgreen"],
    )
    fig.update_traces(
        text=employees_on_leave_per_designation["Total Employees on Leave"],
        textposition="top right",
    )
    fig.update_layout(
        xaxis_title="Designation",
        yaxis_title="Total Employees on Leave",
        yaxis=dict(
            range=[
                -10,
                employees_on_leave_per_designation["Total Employees on Leave"].max()
                + 10,
            ]
        ),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.empty()


# ========= Total leaves per designation
leave_days_by_designation_employee = defaultdict(int)
leave_days_by_designation = defaultdict(int)

for entry in employee_leaves_insight_data["data"]:
    if (
        "employee_designation" in entry
        and "employee_name" in entry
        and "leave_days" in entry
        and entry["status"] in ["APPROVED"]
    ):
        key = (entry["employee_designation"], entry["employee_name"])
        leave_days_by_designation_employee[key] += entry["leave_days"]
        leave_days_by_designation[entry["employee_designation"]] += entry["leave_days"]

# Create a DataFrame for the leave distribution
df_leave_distribution = pd.DataFrame(
    list(leave_days_by_designation_employee.items()),
    columns=["Designation Employee", "Total Leave Days"],
)

# Ensure that the columns are of the same length
if not df_leave_distribution.empty:
    df_leave_distribution[["Designation", "Employee Name"]] = pd.DataFrame(
        df_leave_distribution["Designation Employee"].tolist(),
        index=df_leave_distribution.index,
    )
    df_leave_distribution = df_leave_distribution.drop(columns=["Designation Employee"])

    # Ensure Total Leave Days are integers
    df_leave_distribution["Total Leave Days"] = df_leave_distribution[
        "Total Leave Days"
    ].astype(int)

    # Create a DataFrame for the total leave days by designation
    df_total_leave_by_designation = pd.DataFrame(
        list(leave_days_by_designation.items()),
        columns=["Designation", "Total Leave Days"],
    )

    # Plot the data using Plotly Treemap
    fig = px.treemap(
        df_leave_distribution,
        path=["Designation", "Employee Name"],
        values="Total Leave Days",
        title="Total Leave Days by Designation and Employee",
        color="Total Leave Days",
        color_continuous_scale="Blues",
        hover_data={"Total Leave Days": True},
        height=800,
        width=800,
    )

    # Update hover template to show only label and values
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Total Leave Days: %{value}",
        customdata=[
            df_total_leave_by_designation.set_index("Designation").loc[designation][
                "Total Leave Days"
            ]
            for designation in df_leave_distribution["Designation"]
        ],
    )

    fig.update_traces(root_color="lightgrey")
    fig.update_traces(marker=dict(showscale=True), textinfo="label+value")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")


# ============= Leave Distribution by Fiscal Year ===========
st.divider()
st.caption("Leave Month Info")
leave_days_by_employee_month_date = defaultdict(int)
for entry in employee_leaves_insight_data["data"]:
    if (
        "employee_name" in entry
        and "leave_days" in entry
        and "leave_month_dd" in entry
        and entry["status"] in ["APPROVED"]
    ):
        key = (entry["employee_name"], entry["leave_month_dd"])
        leave_days_by_employee_month_date[key] += entry["leave_days"]

df_leave_distribution = pd.DataFrame(
    list(leave_days_by_employee_month_date.items()),
    columns=["Employee Month Date", "Total Leave Days"],
)
if not df_leave_distribution.empty:
    df_leave_distribution[["Employee Name", "Leave Month Date"]] = pd.DataFrame(
        df_leave_distribution["Employee Month Date"].tolist(),
        index=df_leave_distribution.index,
    )
else:
    df_leave_distribution["Employee Name"] = []
    df_leave_distribution["Leave Month Date"] = []
df_leave_distribution = df_leave_distribution.drop(columns=["Employee Month Date"])

month_order = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

# Extract the month from the leave month date for ordering
# Ensure "Leave Month Date" column contains string values
df_leave_distribution["Leave Month Date"] = df_leave_distribution[
    "Leave Month Date"
].astype(str)

# Handle potential missing or malformed data
df_leave_distribution["Leave Month"] = (
    df_leave_distribution["Leave Month Date"].str[:3].fillna("Unknown")
)
df_leave_distribution["Leave Month Day"] = (
    df_leave_distribution["Leave Month Date"].str[3:].fillna("Unknown")
)

fig = px.bar(
    df_leave_distribution,
    x="Leave Month",
    y="Total Leave Days",
    color="Employee Name",
    title="Total Leave Days over Fiscal Month",
    text="Total Leave Days",
    barmode="group",
    category_orders={"Leave Month": month_order},
    hover_data={"Leave Month Date": True, "Total Leave Days": True},
    height=600,
    width=800,
)
fig.update_layout(xaxis_title="Leave Month Date", yaxis_title="Total Leave Days")

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
