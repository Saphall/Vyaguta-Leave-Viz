import time
import warnings
import streamlit as st

from src.insights.page import home, leave_information, employee
from src.db.utils.database import databaseConnect, databaseDisconnect


st.set_page_config(
    page_title="Vyaguta Leave Viz", layout="wide", initial_sidebar_state="expanded"
)
warnings.filterwarnings("ignore", "pandas only supports SQLAlchemy connectable")


# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Emp Visualization", "Leave Information"])


def main():
    conn = databaseConnect()
    if page == "Home":
        home.main(conn)

    elif page == "Emp Visualization":
        employee.main(conn)

    elif page == "Leave Information":
        leave_information.main(conn)

    databaseDisconnect(conn)


def rerun():
    while True:
        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    main()
    rerun()
