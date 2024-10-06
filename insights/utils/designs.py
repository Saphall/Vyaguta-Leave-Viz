# KPI card
def create_card(title, value, info_1: str = "", info_2: str = ""):
    card_html = f"""
    <div style='
        background: linear-gradient(135deg, #3a3a3a 0%, #1f1f1f 100%);
        background-color: #333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        width: 80%;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5);
        color: #fff;
        font-family: Arial, sans-serif;
        text-align: left;
        cursor: pointer;
    '>
    <h6 style='margin-bottom: 8px; color: #ffcc00;'>{title}</h6>
    <h4 style='margin-bottom: 8px; color: #eef;'>{value}</h4>
    <p style='margin-bottom: 8px; color: #ccc; font-size: 15px;'>{info_1}</p>
    <p style='margin-bottom: 8px; color: #ccc; font-size: 15px;'>{info_2}</p>
    </div>
    """
    return card_html


def create_secondary_card(value, info_1: str = "", info_2: str = ""):
    card_html = f"""
    <div style='
        background: linear-gradient(135deg, #3a3a3a 0%, #1f1f1f 100%);
        background-color: #333;
        border-radius: 8px;
        padding: 20px;
        width: 90%;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5);
        color: #fff;
        font-family: Arial, sans-serif;
        text-align: left;
        cursor: pointer;
    '>
    <h5 style='color: #ffcc00;'>{value}</h5>
    <p style='margin-bottom: 8px; color: #ccc; font-size: 15px;'><b>{info_1}</b></p>
    <p style='margin-bottom: 8px; color: #ccc; font-size: 15px;'><b>{info_2}</b></p>
    </div>
    """
    return card_html


# profile card
def profile_card(name, email: str = "", department: str = ""):
    card_html = f"""
    <div style='
        background: linear-gradient(135deg, #3a3a3a 0%, #1f1f1f 100%);
        background-color: #333;
        border-radius: 15px;
        padding: 20px;
        width: 85%;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5);
        color: #fff;
        font-family: Arial, sans-serif;
        text-align: left;
        cursor: pointer;
    '>
    <h4 style='margin-bottom: 8px; color: #ffcc00;'>{name}</h4>
    <h6 style='margin-bottom: 4px; color: #ddd;'><b>{email}</b></h6>
    <h6 style='margin-bottom: 1px; color: #fff;'><b>Dapartment:</b> {department}</h6>
    </div>
    """
    return card_html


# info card
def info_card(info, title: str = ""):
    card_html = f"""
    <div style='
        background: linear-gradient(135deg, #3a3a3a 0%, #1f1f1f 100%);
        background-color: #333;
        border-radius: 8px;
        padding: 8px;
        margin-bottom: 16px;
        width: 80%;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5);
        color: #fff;
        font-family: Arial, sans-serif;
        text-align: center;
        cursor: pointer;
    '>
    <h5 style='padding: 8px; color: #90cc90;'>{info}</h4>
"""
    return card_html
