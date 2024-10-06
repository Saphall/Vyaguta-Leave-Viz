import streamlit as st

col1, col2, col3 = st.columns(3)

card_html = """
<div class="title">Developer</div>
<br>
<div class="card">
    <img src="https://avatars.githubusercontent.com/u/66344649?v=4" alt="Saphal Shakha" style="width:100%">
    <h2>Saphal Shakha</h2>
    <p class="title">Software Engineer, Data</p>
    <p>Leapfrog Technology</p>
    <p><button><a href="https://github.com/Saphall/Vyaguta-Leave-Viz" target="_blank">
    <img src="https://i.pinimg.com/736x/b5/1b/78/b51b78ecc9e5711274931774e433b5e6.jpg" alt="GitHub" style="width:32px;height:32px;">
    </button></p>
</div>
"""


st.markdown(
    """
<style>
.card {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    max-width: 300px;
    margin: auto;
    text-align: center;
    font-family: arial;
}

.title {
    color: grey;
    font-size: 18px;
    text-align: center;
}

button {
    border: none;
    outline: 0;
    display: inline-block;
    padding: 8px;
    color: white;
    background-color: #000;
    text-align: center;
    cursor: pointer;
    width: 100%;
    font-size: 16px;
}

a {
    text-decoration: none;
    color: black;
}

button:hover, a:hover {
    opacity: 0.7;
}
</style>
""",
    unsafe_allow_html=True,
)


with col2:
    st.write("")
    st.markdown(card_html, unsafe_allow_html=True)
