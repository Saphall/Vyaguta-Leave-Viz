import streamlit as st
from genderize import Genderize
from genderize import Genderize, GenderizeException


# return gender from the employee full name
def get_gender(employee_name, full_name=True):
    if full_name:
        first_name = employee_name.split()[0]
    else:
        first_name = employee_name
    genderize = Genderize()
    try:
        result = genderize.get([first_name])
        if result[0]["probability"] > 0.5:
            return result[0]["gender"]
    except GenderizeException:
        return
    return


# profile pic for the employee
@st.cache_data
def profile_pic(gender: None):
    if gender == "male":
        return (
            "https://lottie.host/9114c915-18d6-4082-8760-56d7620e22cb/xq3vCQM2Kq.json"
        )
        # "https://lottie.host/3012c7b0-e872-47b9-9976-7966ef09f859/1meTNowpx8.json"
    elif gender == "female":
        return (
            "https://lottie.host/9144eec3-e92e-4335-ade7-abaead4642cd/xAsJ17SOva.json"
        )
        # "https://lottie.host/e314d900-9dd9-43c4-94a4-9bf236c08d78/059jAGdOoi.json"
    return "https://lottie.host/e30530fd-b133-4f1a-9754-4350e9c9484c/vy2fwj1bwm.json"
