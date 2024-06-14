import json
from fastapi import Request
from fastapi.responses import JSONResponse
from src.db.utils.database import databaseConnect, databaseDisconnect
from .services import get_leave_info, insert_leave_info


async def fetch_leaves(request: Request):
    if (auth_header := request.headers.get("Authorization")) is None:
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


async def load_leaves(bearer_token: str):
    response = await get_leave_info(bearer_token)

    try:
        data = response.json()["data"]
        conn = databaseConnect()
        await insert_leave_info(data, conn)
        databaseDisconnect(conn)
        print("INFO: Leave Data Inserted Successfully!")
        return {"success": "Leave Data Inserted Successfully!"}, 200
    except KeyError as e:
        print("INFO: Leave Data Insert Failed. Couldn't fetch the leave data!")
        return {"error": f"Couldn't insert the leave data! {e}"}
    except json.JSONDecodeError as e:
        print(f"INFO: Couldn't decode the JSON response! JSONDecodeError:{e}")
        return {
            "error": f"Leave Data Insert Failed. Couldn't decode the JSON response! {e}"
        }


async def handle_leaves_request(request: Request):
    if (auth_header := request.headers.get("Authorization")) is None:
        return {"error": "No Authorization header found"}, 401

    bearer_token = auth_header.replace("Bearer ", "", 1)
    result = await load_leaves(bearer_token)
    return JSONResponse(content=result, status_code=200)
