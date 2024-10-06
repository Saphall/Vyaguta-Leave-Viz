import requests
import streamlit as st

from insights.utils.constants import BACKEND_SERVER


@st.cache_data
def get_api_data(url, query=None):
    if query:
        response = requests.get(url, params=query)
    else:
        response = requests.get(url)
    return response.json()


# API datas
employees_data = get_api_data(f"{BACKEND_SERVER}/api/employees")["data"]
designations_data = get_api_data(f"{BACKEND_SERVER}/api/designations")["data"]
allocations_data = get_api_data(f"{BACKEND_SERVER}/api/allocations")["data"]
departments_data = get_api_data(f"{BACKEND_SERVER}/api/departments")["data"]
leave_types_data = get_api_data(f"{BACKEND_SERVER}/api/leave_types")["data"]
fiscal_year_data = get_api_data(f"{BACKEND_SERVER}/api/fiscal_year")["data"]
