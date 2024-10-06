import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

from streamlit_lottie import st_lottie

from insights import assets
from insights.utils.util import get_gender, profile_pic
from insights.utils.api import get_api_data, leave_types_data
from insights.utils.designs import profile_card, create_secondary_card, info_card
from collections import defaultdict
from insights.utils.constants import (
    EMPLOYEE_LEAVES_INSIGHT_URL,
    EMPLOYEE_DETAILS_INSIGHT_URL,
)
from insights.utils.filters import (
    employee_names_filter_values,
    leave_types_filter_values,
    fiscal_year_filter_values,
    min_start_date,
)


# ================ Filter Values ========================
st.caption(":material/tune: Filters")
col1, col2, col3, col4, col5 = st.columns([0.4, 0.4, 0.4, 1, 0.4])
# ===== Filter: leave_types
leave_type_popover = col1.popover(
    ":material/filter_alt: Leave Type", help="Leave Type filter for visualization"
)
selected_leave_types = leave_type_popover.multiselect(
    ":palm_tree: Leave Types",
    leave_types_filter_values,
)

# ===== Filter leave_status
leave_status_popover = col2.popover(
    ":material/filter_alt: Leave Status", help="Leave Status filter for visualization"
)
selected_leave_status = leave_status_popover.multiselect(
    ":traffic_light: Leave Status",
    ["APPROVED", "REQUESTED", "REJECTED", "CANCELLED"],
)

# ===== Filter: fiscal_year
fiscal_year_popover = col3.popover(
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

selected_start_date_range = col4.slider(
    "Date Range:",
    min_value=start_date,
    max_value=end_of_year_date,
    value=(min_start_date, current_date),
    format="YYYY-MM-DD",
    help="Select the date range for the leave data",
)
selected_start_date, selected_end_date = selected_start_date_range

st.divider()


# ===== Filter: Employee Name
col1, col2 = st.columns([0.3, 1])
selected_employee_name = col1.selectbox(
    ":material/person: Employee Name", sorted(employee_names_filter_values)
)
st.markdown("<br>", unsafe_allow_html=True)


# ==============Fetch Insights Data=================
query_params = {}
if selected_leave_types:
    query_params["leave_type"] = selected_leave_types
if selected_leave_status:
    query_params["leave_status"] = selected_leave_status
if selected_fiscal_years:
    query_params["fiscal_date"] = selected_fiscal_years
if selected_start_date and selected_end_date:
    query_params["start_date"] = selected_start_date
    query_params["end_date"] = selected_end_date
if selected_employee_name:
    query_params["employee_name"] = selected_employee_name


# Selected employee details all data
all_employee_details = get_api_data(
    EMPLOYEE_DETAILS_INSIGHT_URL, query={"employee_name": selected_employee_name}
)
# Filtered employee details data
filtered_employee_details = get_api_data(
    EMPLOYEE_DETAILS_INSIGHT_URL, query=query_params
)

# Employee leaves insight data
employee_leaves_insight_data = get_api_data(
    EMPLOYEE_LEAVES_INSIGHT_URL, query=query_params
)


# ================================================================
# ================== Employee Profile Overview ===================
col1, col2, col3, col4 = st.columns([0.5, 1, 1, 1])

with col1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    try:
        st_lottie(
            profile_pic(get_gender(selected_employee_name)),
            height=200,
            width=240,
            key="profile_animation",
        )
    except Exception:
        st.image(f"{assets.__path__[0]}/profile_pic.png", use_column_width=True)

# Extract email
email = list(
    dict.fromkeys(
        [data["email"] for data in all_employee_details["data"] if "email" in data]
    )
)
employee_email = email[-1] if len(email) == 1 else "Unknown"

# Extract department
department = list(
    dict.fromkeys(
        [
            data["employee_department"]
            for data in filtered_employee_details["data"]
            if "employee_department" in data
        ]
    )
)
employee_department = department[-1] if len(department) == 1 else "Unknown"

# Extract designation
designation = list(
    dict.fromkeys(
        [
            data["employee_designation"]
            for data in all_employee_details["data"]
            if "employee_designation" in data
        ]
    )
)
employee_designation = designation[-1] if len(designation) == 1 else "Unknown"

# Extract leave issuer
leave_issuer = list(
    dict.fromkeys(
        [
            data.get("leave_issuer_name", "Unknown")
            for data in filtered_employee_details["data"]
            if data.get("leave_issuer_name") is not None
        ]
    )
)
employee_leave_issuer = leave_issuer[-1] if len(leave_issuer) == 1 else "Unknown"

# Extract leave issuer email
leave_issuer_email = list(
    dict.fromkeys(
        [
            data.get("leave_issuer_email", "Unknown")
            for data in filtered_employee_details["data"]
            if data.get("leave_issuer_email") is not None
        ]
    )
)
employee_leave_issuer_email = (
    leave_issuer_email[-1] if len(leave_issuer_email) == 1 else "Unknown"
)


with col2:
    # st.write("")
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Employee Detail")
    st.markdown(
        profile_card(selected_employee_name, employee_email, employee_department),
        unsafe_allow_html=True,
    )

with col3:
    st.caption("Designation")
    st.markdown(info_card(info=employee_designation), unsafe_allow_html=True)
    st.write("")
    st.caption("Leave Issuer")
    st.markdown(
        create_secondary_card(
            value=employee_leave_issuer, info_1=employee_leave_issuer_email
        ),
        unsafe_allow_html=True,
    )


with col4:
    allocation_df = pd.DataFrame(filtered_employee_details["data"])
    if all(
        col in allocation_df.columns for col in ["allocation_name", "allocation_type"]
    ):
        allocations_detail = (
            allocation_df[["allocation_name", "allocation_type"]]
            .dropna()
            .drop_duplicates()
        )
    else:
        allocations_detail = pd.DataFrame(
            columns=["allocation_name", "allocation_type"]
        )
    st.write("")
    st.caption("Allocations Detail")
    allocations_detail.index = range(1, len(allocations_detail) + 1)
    st.dataframe(allocations_detail, height=213, use_container_width=True)

st.divider()


# =================================================================
# ================== Leave Days by Leave Type =====================
st.caption("Leaves Info")
col1, col2, col3 = st.columns([0.35, 1, 0.35])

df = pd.DataFrame(employee_leaves_insight_data["data"])
if "leave_type" not in df.columns:
    df["leave_type"] = pd.Series(dtype="str")
if "leave_days" not in df.columns:
    df["leave_days"] = pd.Series(0, dtype="float")

df_grouped = df.groupby("leave_type")["leave_days"].sum().reset_index()
all_leave_types_df = pd.DataFrame(
    {
        "leave_type": leave_types_filter_values,
        "leave_days": [0] * len(leave_types_filter_values),
    }
)
df_final = pd.merge(all_leave_types_df, df_grouped, on="leave_type", how="left").fillna(
    0
)
df_final["leave_days"] = df_final["leave_days_y"].astype(int)
df_final = df_final[["leave_type", "leave_days"]]

# Order by leave days descending
df_final = df_final.sort_values(by="leave_type").reset_index(drop=True)

# Start the dataframe index from 1
df_final.index = df_final.index + 1

with col1:
    st.write("")
    st.write("Total Leave Records")
    st.dataframe(df_final)

with col2:
    fig = px.bar(
        df_final,
        x="leave_type",
        y="leave_days",
        title="Leave Records by Leave Type and Status",
        text="leave_days",
    )
    fig.update_traces(marker=dict(color="SlateBlue", colorscale="Viridis"))
    st.plotly_chart(fig)


with col3:
    if "status" not in df.columns:
        df["status"] = pd.Series(dtype="str")

    leave_status_counts = df.groupby(["status"]).size().reset_index(name="count")
    custom_colors = {
        "APPROVED": "darkgreen",
        "REQUESTED": "lightgreen",
        "REJECTED": "indianred",
        "CANCELLED": "darksalmon",
    }
    fig = px.pie(
        leave_status_counts,
        values="count",
        names="status",
        title="Leave Status Info",
        hole=0.4,
        color="status",
        color_discrete_map=custom_colors,
    )
    st.plotly_chart(fig)

st.divider()


# =================================================================
# ====================  Leave Balance =============================
st.caption("Leave Balance Info")

df = (
    pd.DataFrame(employee_leaves_insight_data["data"])
    if employee_leaves_insight_data["data"]
    else pd.DataFrame()
)
if "status" in df.columns:
    df_filtered = df[df["status"].isin(["APPROVED", "REQUESTED"])]
else:
    df_filtered = pd.DataFrame(columns=df.columns)

if "leave_type" not in df_filtered.columns:
    df_filtered["leave_type"] = pd.Series(dtype="str")
if "leave_days" not in df_filtered.columns:
    df_filtered["leave_days"] = pd.Series(0, dtype="float")

df_grouped = df_filtered.groupby("leave_type")["leave_days"].sum().reset_index()
all_leave_types_df = pd.DataFrame(
    {
        "leave_type": leave_types_filter_values,
        "leave_days": [0] * len(leave_types_filter_values),
    }
)
df_final = pd.merge(all_leave_types_df, df_grouped, on="leave_type", how="left").fillna(
    0
)
df_final["leave_days"] = df_final["leave_days_y"].astype(int)
df_final = df_final[["leave_type", "leave_days"]]

# Order by leave days descending
df_final = df_final.sort_values(by="leave_type").reset_index(drop=True)

# Start the dataframe index from 1
df_final.index = df_final.index + 1


leave_types_df = pd.DataFrame(leave_types_data)
merged_df = pd.merge(leave_types_df, df_final, on="leave_type", how="left")

# Calculate leave_balance
merged_df["leave_balance"] = merged_df["default_days"] - merged_df["leave_days"]
merged_df["leave_balance"] = merged_df["leave_balance"].apply(lambda x: max(x, 0))

# Rename columns
result_df = merged_df[
    ["leave_type", "default_days", "leave_days", "leave_balance"]
].dropna(subset=["leave_type"])
result_df.columns = ["leave_type", "default", "taken", "balance"]
result_df = result_df.sort_values(by="leave_type").reset_index(drop=True)
result_df.index = result_df.index + 1


col1, col2 = st.columns([0.4, 1])
with col1:
    st.write("")
    st.write("Total Leave balance")
    st.dataframe(result_df)


with col2:
    fig_bar = px.bar(
        result_df.melt(
            id_vars="leave_type", value_vars=["default", "taken", "balance"]
        ),
        x="leave_type",
        y="value",
        color="variable",
        barmode="relative",
        text_auto=True,
        color_discrete_map={
            "default": "lightblue",
            "taken": "lightcoral",
            "balance": "mediumseagreen",
        },
        title="Leave Balance by Leave Type",
    )
    fig_bar.update_layout(
        xaxis_title="Leave Type",
        yaxis_title="Days",
        legend_title="Leave Category",
        title_x=0.5,
        template="plotly_white",
    )
    st.plotly_chart(fig_bar)


st.divider()

# =================================================================
# =================== Leave over Time ==============================
st.caption("Leave Trend")

leave_days_by_employee_month_date = defaultdict(int)
for entry in employee_leaves_insight_data["data"]:
    if (
        "employee_name" in entry
        and "leave_days" in entry
        and "leave_month_dd" in entry
        and entry["status"] in ["APPROVED", "REQUESTED"]
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

# Ensure "Leave Month Date" column contains string values
df_leave_distribution["Leave Month Date"] = df_leave_distribution[
    "Leave Month Date"
].astype(str)

# Convert "Leave Month Date" to datetime for proper plotting
df_leave_distribution["Leave Month Date"] = pd.to_datetime(
    df_leave_distribution["Leave Month Date"], format="%b%d"
)

# Filter data for the selected employee
employee_leave_data = df_leave_distribution[
    df_leave_distribution["Employee Name"] == selected_employee_name
]

# Plot the area chart with smoothed lines
fig_area = px.area(
    employee_leave_data,
    x="Leave Month Date",
    y="Total Leave Days",
    title=f"Leave Days Over Months",
    markers=True,
)

fig_area.update_traces(line_shape="spline")

fig_area.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Leave Days",
    xaxis=dict(tickformat="%b %d"),
    yaxis=dict(range=[-1, employee_leave_data["Total Leave Days"].max() + 1]),
    annotations=[
        dict(
            x=employee_leave_data["Leave Month Date"].iloc[i],
            y=employee_leave_data["Total Leave Days"].iloc[i],
            text=str(employee_leave_data["Total Leave Days"].iloc[i]),
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-20,
        )
        for i in range(len(employee_leave_data))
    ],
)
st.plotly_chart(fig_area, use_container_width=True)

# =============== Leave records ========================
st.caption("Leave Records")


def highlight_status(row):
    color = "indianred" if row["status"] in ["REJECTED", "CANCELLED"] else ""
    return ["background-color: {}".format(color) for _ in row]


leave_records = (
    pd.DataFrame(employee_leaves_insight_data["data"])
    if employee_leaves_insight_data["data"]
    else pd.DataFrame()
)

leave_records["leave_issuer_name"] = (
    leave_records.get("leave_issuer_first_name", "")
    + " "
    + leave_records.get("leave_issuer_last_name", "")
)
selected_columns = [
    "leave_type",
    "leave_days",
    "start_date",
    "end_date",
    "reason",
    "status",
    "leave_issuer_name",
]
leave_records = leave_records.reindex(columns=selected_columns, fill_value="").dropna(
    subset=selected_columns[:-1]
)

leave_records["leave_days"] = (
    pd.to_numeric(leave_records["leave_days"], errors="coerce").fillna(0).astype(int)
)

leave_records = leave_records.sort_values(by="start_date")
leave_records.index = range(1, len(leave_records) + 1)
leave_records["start_date"] = pd.to_datetime(leave_records["start_date"]).dt.strftime(
    "%b %d, %Y"
)
leave_records["end_date"] = pd.to_datetime(leave_records["end_date"]).dt.strftime(
    "%b %d, %Y"
)

st.dataframe(
    leave_records.style.apply(highlight_status, axis=1), use_container_width=True
)
