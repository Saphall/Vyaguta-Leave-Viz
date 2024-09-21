import pandas as pd
import streamlit as st
import plotly.express as px


def main(conn):
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
