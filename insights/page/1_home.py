import streamlit as st
import streamlit.components.v1 as components

st.title(":frog: Leave Visualization Dashboard")

col1, col2 = st.columns([1, 0.7])

with col1:
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.write("##### Welcome to the Leave Visualization Dashboard!")
    st.caption("This is a Streamlit Dashboard to visualize leave data.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)

    popover = st.popover(
        "Data Source", help="Data Source for visualization", disabled=True
    )
    api = popover.radio("Data Source", ("Use API Data", "Upload File"))
    if api == "Use API Data":
        st.success("API Data Selected: **Vyaguta API**")
    else:
        uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx", "json"])

        if uploaded_file is not None:
            file_type = uploaded_file.name.split(".")[-1]
            st.write(f"File uploaded: `{uploaded_file.name}` ({file_type.upper()})")


with col2:
    components.iframe(
        "https://lottie.host/embed/0f3d67af-051d-465b-9ce3-959566a8abee/LSl0Pe2W88.json",
        width=500,
        height=500,
    )
