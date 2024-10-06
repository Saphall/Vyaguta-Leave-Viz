import pandas as pd

from insights.utils.api import (
    leave_types_data,
    fiscal_year_data,
    departments_data,
    designations_data,
    allocations_data,
    employees_data,
)

# ===== Filter: fiscal_years
fiscal_year_filter_values = [
    f"{item['start_date'][:4]}/{item['end_date'][:4]}"
    for item in fiscal_year_data
    if "start_date" in item and "end_date" in item
]

# ===== Filter: deparments
department_filter_values = [
    item["department_name"]
    for item in departments_data
    if "department_name" in item and "department_id" in item
]

# ===== Filter: leave_types
leave_types_filter_values = [
    item["leave_type"]
    for item in leave_types_data
    if "leave_type" in item and "leave_type_id" in item
]

# ===== Filter: designations
designation_filter_values = [
    item["designation_name"]
    for item in designations_data
    if "designation_name" in item and "designation_id" in item
]

# ===== Filter: allocations
allocation_filter_values = [
    item["name"]
    for item in allocations_data
    if "name" in item and "allocation_id" in item and item["type"] == "project"
]

# ===== Filter: employee_names
employee_names_filter_values = [
    item["first_name"] + " " + item["last_name"]
    for item in employees_data
    if "first_name" in item and "last_name" in item
]

# ===== Filter: start_date
start_date_filter_values = [
    item["start_date"] for item in fiscal_year_data if "start_date" in item
]
min_start_date = pd.to_datetime(start_date_filter_values).min().date()
