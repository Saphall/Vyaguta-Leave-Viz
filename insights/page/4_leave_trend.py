import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

from collections import defaultdict

from viz.utils.api import get_api_data
from viz.utils.constants import EMPLOYEE_LEAVES_INSIGHT_URL
from viz.utils.filters import fiscal_year_filter_values, min_start_date


st.caption(":material/tune: Filters")
col1, col2, col3, col4, col5 = st.columns([0.4, 1, 0.4, 0.4, 0.4])
# ==== Filter: fiscal_year
fiscal_year_popover = col1.popover(
    ":material/filter_alt: Fiscal Year", help="Fiscal Year filter for visualization"
)
selected_fiscal_years = fiscal_year_popover.multiselect(
    ":date: Fiscal Years",
    fiscal_year_filter_values,
)

# ==== Filter: start_date
start_date = min_start_date.replace(month=1, day=1)
current_date = datetime.datetime.now().date()
end_of_year_date = current_date.replace(month=12, day=31)

selected_start_date_range = col2.slider(
    "Date Range:",
    min_value=start_date,
    max_value=end_of_year_date,
    value=(min_start_date, current_date),
    format="YYYY-MM-DD",
    help="Select the date range for the leave data",
)
selected_start_date, selected_end_date = selected_start_date_range

st.divider()


# ==============Fetch Insights Data=================
query_params = {}
if selected_fiscal_years:
    query_params["fiscal_date"] = selected_fiscal_years
if selected_start_date and selected_end_date:
    query_params["start_date"] = selected_start_date
    query_params["end_date"] = selected_end_date

# Employee leaves insight data
employee_leaves_insight_data = get_api_data(
    EMPLOYEE_LEAVES_INSIGHT_URL, query=query_params
)


# =======================================================================
# ============== Total Employees on Leave Over Time =======================
st.caption("Employees on Leave Trend")
employees_on_leave_by_month = defaultdict(int)
month_mapping = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

for entry in employee_leaves_insight_data["data"]:
    if (
        "leave_year" in entry
        and "leave_month" in entry
        and entry["status"] in ["APPROVED"]
    ):
        leave_year = int(entry["leave_year"])
        leave_month = entry["leave_month"]
        if isinstance(leave_month, str):
            leave_month = month_mapping.get(leave_month, 0)
        else:
            leave_month = int(leave_month)
        key = f"{leave_year}-{leave_month:02d}"
        employees_on_leave_by_month[key] += 1

# Convert to DataFrame and sort by Month
df_employees_on_leave = pd.DataFrame(
    list(employees_on_leave_by_month.items()),
    columns=["Month", "Total Employees on Leave"],
)
df_employees_on_leave["Month"] = pd.to_datetime(
    df_employees_on_leave["Month"], format="%Y-%m"
)
df_employees_on_leave = df_employees_on_leave.sort_values("Month")

# Plot the data with a curved line
fig_employees_on_leave = px.line(
    df_employees_on_leave,
    x="Month",
    y="Total Employees on Leave",
    title="Employees on Leave Over Time",
    markers=True,
    text="Total Employees on Leave",
    line_shape="spline",
)
fig_employees_on_leave.update_traces(textposition="top right")

st.plotly_chart(fig_employees_on_leave, use_container_width=True)


# =================Total Employees on Leave by Year =======================
col1, col2 = st.columns([1, 1])
year_employee_data = defaultdict(int)

for entry in employee_leaves_insight_data["data"]:
    if "leave_year" in entry and entry["status"] in ["APPROVED"]:
        leave_year = entry["leave_year"]
        year_employee_data[leave_year] += 1

df_year_employee = pd.DataFrame(
    list(year_employee_data.items()), columns=["Year", "Total Employees on Leave"]
)
df_year_employee = df_year_employee.sort_values("Year")

with col1:
    fig_year_employee = px.area(
        df_year_employee,
        x="Year",
        y="Total Employees on Leave",
        title="Total Employees on Leave by Year",
        markers=True,
        text="Total Employees on Leave",
        line_shape="spline",
    )
    fig_year_employee.update_traces(
        textposition="top right", line_color="orange", fillcolor="rgba(255,165,0,0.2)"
    )

    st.plotly_chart(fig_year_employee, use_container_width=True)


# ================= Total Employees on Leave by Month =======================
month_employee_data = defaultdict(int)

for entry in employee_leaves_insight_data["data"]:
    if "leave_month" in entry and entry["status"] in ["APPROVED"]:
        leave_month = entry["leave_month"]
        month_employee_data[leave_month] += 1

# Convert to DataFrame and sort by Month (Jan to Dec)
df_month_employee = pd.DataFrame(
    list(month_employee_data.items()), columns=["Month", "Total Employees on Leave"]
)
df_month_employee["Month"] = pd.Categorical(
    df_month_employee["Month"],
    categories=[
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
    ],
    ordered=True,
)
df_month_employee = df_month_employee.sort_values("Month")

with col2:
    fig_month_employee = px.area(
        df_month_employee,
        x="Month",
        y="Total Employees on Leave",
        title="Total Employees on Leave by Month",
        markers=True,
        text="Total Employees on Leave",
        line_shape="spline",
    )
    fig_month_employee.update_traces(
        textposition="top right",
        line_color="lightgreen",
        fillcolor="rgba(144,238,144,0.2)",
    )

    st.plotly_chart(fig_month_employee, use_container_width=True)

# ==================Total employee on leave by week =======================
col1, col2 = st.columns([1, 0.05])
week_employee_data = defaultdict(int)

for entry in employee_leaves_insight_data["data"]:
    if "leave_day" in entry and entry["status"] in ["APPROVED"]:
        week = entry["leave_day"]
        week_employee_data[week] += 1

# Define the order of the days from SUN to SAT
week_order = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

# Convert to DataFrame and sort by the defined week order
df_week_employee = pd.DataFrame(
    list(week_employee_data.items()), columns=["Week", "Total Employees on Leave"]
)
df_week_employee["Week"] = pd.Categorical(
    df_week_employee["Week"], categories=week_order, ordered=True
)
df_week_employee = df_week_employee.sort_values("Week")

with col1:
    fig_week_employee = px.area(
        df_week_employee,
        x="Week",
        y="Total Employees on Leave",
        title="Total Employees on Leave by Week",
        markers=True,
        text="Total Employees on Leave",
        line_shape="spline",
    )
    fig_week_employee.update_traces(
        textposition="top right",
        line_color="lightyellow",
        fillcolor="rgba(255,255,224,0.2)",
    )

    st.plotly_chart(fig_week_employee, use_container_width=True)

st.markdown(
    """
    <style>
    .label-darkyellow {
        background-color: darkkhaki;
        padding: 5px;
        border-radius: 5px;
        color: black;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
    }
    .label-lightgreen {
        background-color: lightgreen;
        padding: 5px;
        border-radius: 5px;
        color: black;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
    }
    .label-lightyellow {
        background-color: lightyellow;
        padding: 5px;
        border-radius: 5px;
        color: black;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
    }
    .label-icon {
        margin-right: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with col2:
    st.write("")
    st.caption("Legend")
    st.markdown(
        '<div class="label-darkyellow"></span>Year</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="label-lightgreen"></span>Month</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="label-lightyellow"></span>Week</div>', unsafe_allow_html=True
    )

st.divider()


# =====================================================================
# ================== Total Leave Days Over Time =======================
st.caption("Leave Days Trend")
leave_days_by_month = defaultdict(int)

for entry in employee_leaves_insight_data["data"]:
    if (
        "leave_year" in entry
        and "leave_month" in entry
        and "leave_days" in entry
        and entry["status"] in ["APPROVED"]
    ):
        leave_year = int(entry["leave_year"])
        leave_month = entry["leave_month"]
        if isinstance(leave_month, str):
            leave_month = month_mapping.get(leave_month, 0)
        else:
            leave_month = int(leave_month)
        key = f"{leave_year}-{leave_month:02d}"
        leave_days_by_month[key] += entry["leave_days"]

# Convert to DataFrame and sort by Month
df_leave_trends = pd.DataFrame(
    list(leave_days_by_month.items()), columns=["Month", "Total Leave Days"]
)
df_leave_trends["Month"] = pd.to_datetime(df_leave_trends["Month"], format="%Y-%m")
df_leave_trends = df_leave_trends.sort_values("Month")

# Plot the data with a curved line
fig_trends = px.line(
    df_leave_trends,
    x="Month",
    y="Total Leave Days",
    title="Leave Days Over Time",
    markers=True,
    text="Total Leave Days",
    line_shape="spline",
)
fig_trends.update_traces(textposition="top right")

st.plotly_chart(fig_trends, use_container_width=True)


# =================Total Leave Days by Year =======================
col1, col2 = st.columns([1, 1])
year_leave_data = defaultdict(int)

for entry in employee_leaves_insight_data["data"]:
    if (
        "leave_year" in entry
        and "leave_days" in entry
        and entry["status"] in ["APPROVED"]
    ):
        leave_year = entry["leave_year"]
        leave_days = entry["leave_days"]
        year_leave_data[leave_year] += leave_days

df_year_leave = pd.DataFrame(
    list(year_leave_data.items()), columns=["Year", "Total Leave Days"]
)
df_year_leave = df_year_leave.sort_values("Year")
with col1:
    fig_year_leave = px.area(
        df_year_leave,
        x="Year",
        y="Total Leave Days",
        title="Leave Days by Year",
        markers=True,
        text="Total Leave Days",
        line_shape="spline",
    )
    fig_year_leave.update_traces(
        textposition="top right", line_color="orange", fillcolor="rgba(255,165,0,0.2)"
    )

    st.plotly_chart(fig_year_leave, use_container_width=True)


# =================Total Leave Days by Month =======================
month_leave_data = defaultdict(int)

for entry in employee_leaves_insight_data["data"]:
    if (
        "leave_month" in entry
        and "leave_days" in entry
        and entry["status"] in ["APPROVED"]
    ):
        leave_month = entry["leave_month"]
        leave_days = entry["leave_days"]
        month_leave_data[leave_month] += leave_days

# Convert to DataFrame and sort by Month (Jan to Dec)
df_month_leave = pd.DataFrame(
    list(month_leave_data.items()), columns=["Month", "Total Leave Days"]
)
df_month_leave["Month"] = pd.Categorical(
    df_month_leave["Month"],
    categories=[
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
    ],
    ordered=True,
)
df_month_leave = df_month_leave.sort_values("Month")

with col2:
    fig_month_leave = px.area(
        df_month_leave,
        x="Month",
        y="Total Leave Days",
        title="Leave Days by Month",
        markers=True,
        text="Total Leave Days",
        line_shape="spline",
    )
    fig_month_leave.update_traces(
        textposition="top right",
        line_color="lightgreen",
        fillcolor="rgba(144,238,144,0.2)",
    )

    st.plotly_chart(fig_month_leave, use_container_width=True)


# =================Total Leave Days by week =======================
col1, col2 = st.columns([1, 0.05])
week_leave_data = defaultdict(int)
for entry in employee_leaves_insight_data["data"]:
    if (
        "leave_day" in entry
        and "leave_days" in entry
        and entry["status"] in ["APPROVED"]
    ):
        week = entry["leave_day"]
        leave_days = entry["leave_days"]
        week_leave_data[week] += leave_days

# Define the order of the days from SUN to SAT
week_order = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

# Convert to DataFrame and sort by the defined week order
df_week_leave = pd.DataFrame(
    list(week_leave_data.items()), columns=["Week", "Total Leave Days"]
)
df_week_leave["Week"] = pd.Categorical(
    df_week_leave["Week"], categories=week_order, ordered=True
)
df_week_leave = df_week_leave.sort_values("Week")

with col1:
    fig_week_leave = px.area(
        df_week_leave,
        x="Week",
        y="Total Leave Days",
        title="Leave Days by Week",
        markers=True,
        text="Total Leave Days",
        line_shape="spline",
    )
    fig_week_leave.update_traces(
        textposition="top right",
        line_color="lightyellow",
        fillcolor="rgba(255,255,224,0.2)",
    )

    st.plotly_chart(fig_week_leave, use_container_width=True)

with col2:
    st.write("")
    st.caption("Legend")
    st.markdown(
        '<div class="label-darkyellow"></span>Year</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="label-lightgreen"></span>Month</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="label-lightyellow"></span>Week</div>', unsafe_allow_html=True
    )
