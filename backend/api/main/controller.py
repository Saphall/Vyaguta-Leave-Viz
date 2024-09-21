import os
import json
from fastapi import Request
from fastapi.responses import JSONResponse

from .services import get_leave_info, insert_leave_info
from db.utils.database import databaseConnect, databaseDisconnect


async def fetch_leaves(request: Request):
    if (
        auth_header := request.headers.get("Authorization") or os.getenv("BEARER_TOKEN")
    ) is None:
        return {"error": "No Authorization header found"}, 401

    bearer_token = auth_header.replace("Bearer ", "", 1)
    response = await get_leave_info(bearer_token)

    if isinstance(response, dict):
        return JSONResponse(content=response, status_code=response["status_code"])
    return (
        response.json()
        if response.status_code == 200
        else {"error": "Failed to fetch Vyaguta Leave data"}
    ), response.status_code


job_running = False  # Global flag to track if the job is running


async def insert_leaves(bearer_token: str):
    global job_running
    if job_running:
        print("Job already running. Skipping this run.")
        return {"error": "Job already running. Skipping this run."}, 429

    job_running = True

    try:
        # Fetch leave info from Vyaguta
        response = await get_leave_info(bearer_token)

        # Check if the response is valid
        if response.status_code == 200:
            response_json = response.json()

            # Check if "data" exists and is non-empty
            if response_json.get("data"):
                data = response_json["data"]

                # Proceed with database connection and insertion
                conn = await databaseConnect()
                insert_data = await insert_leave_info(data, conn)
                await databaseDisconnect(conn)

                return insert_data.get("success") or insert_data.get(
                    "error"
                ), insert_data.get("status_code", 500)
            else:
                return {"error": "No data received from Vyaguta!"}, 400
        else:
            return {
                "error": f"Failed to fetch Vyaguta Leave data. Status Code: {response.status_code}"
            }, response.status_code

    except KeyError as e:
        return {"error": f"Couldn't insert the leave data! {e}"}, 500
    except json.JSONDecodeError as e:
        return {"error": f"Couldn't decode the JSON response! {e}"}, 500
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}, 500
    finally:
        job_running = False


async def handle_leaves_request(request: Request):
    if (auth_header := request.headers.get("Authorization")) is None:
        return {"error": "No Authorization header found"}, 401

    bearer_token = auth_header.replace("Bearer ", "", 1)
    result = await insert_leaves(bearer_token)
    return JSONResponse(content=result, status_code=200)
