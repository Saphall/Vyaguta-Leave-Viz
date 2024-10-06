import os
from dotenv import load_dotenv

load_dotenv()

# Backend Server
BACKEND_SERVER = os.getenv("BACKEND_SERVER", "http://localhost:8000")

# Employee Details Insight URL
EMPLOYEE_DETAILS_INSIGHT_URL = f"{BACKEND_SERVER}/api/employee_details_insight"
# Employee Leaves Insight URL
EMPLOYEE_LEAVES_INSIGHT_URL = f"{BACKEND_SERVER}/api/employee_leaves_insight"
