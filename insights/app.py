import streamlit as st

st.set_page_config(
    page_title="Vyaguta Leave Viz",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":palm_tree:",
)


home_page = st.Page("page/1_home.py", title="Home", icon=":material/home:")
overview_page = st.Page(
    "page/2_overview.py", title="Overview", icon=":material/dashboard:"
)
employee_page = st.Page(
    "page/3_employee.py", title="Employee", icon=":material/person:"
)
leave_trends_page = st.Page(
    "page/4_leave_trend.py", title="Leave Trend", icon=":material/trending_up:"
)
about_page = st.Page("page/5_about.py", title="About", icon=":material/info:")


pg = st.navigation(
    {
        "": [home_page],
        "Reports": [overview_page, employee_page, leave_trends_page],
        "About": [about_page],
    }
)

pg.run()
