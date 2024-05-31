import streamlit as st
import plotly.graph_objects as go

from src.insights import sql
from src.insights.dashboard import reload
from src.insights.utils.sql import fetch_data


def main():
    # Fetch data
    data = fetch_data(f"{sql.__path__[0]}/employee_details.sql")
    alloc_data = fetch_data(f"{sql.__path__[0]}/allocation_details.sql")
    leave_data = fetch_data(f"{sql.__path__[0]}/leave_balance.sql")

    if data is None or alloc_data is None or leave_data is None:
        print("Failed to fetch data. Please check the logs for details.")
        return

    st.subheader("Employee Details")

    # Convert two columns of DataFrame into dictionary
    result_dict = dict(zip(data["full_name"], data["employee_id"]))

    # Select box
    selected_display_value = st.sidebar.selectbox(
        "Select an option:", sorted(list(result_dict.keys()))
    )

    # Retrieve the associated variable based on the selected display value
    selected_associated_variable = result_dict.get(selected_display_value)

    if selected_associated_variable is None:
        print("Failed to retrieve selected employee details.")
        return

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
    print("Streamlit app executed successfully.")


if __name__ == "__main__":
    main()
    reload()
