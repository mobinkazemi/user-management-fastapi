from http.client import HTTPException
from auth.functions.get_user_or_error import get_user_or_error
from shared.dto.response.api_responseDto import SuccessResponseDto
from fastapi import APIRouter, Depends
import requests
import configparser
import json
from typing import Annotated
from fastapi import Header

config = configparser.ConfigParser()
config.read("config.ini")

FASTAPI_URL = config.get("postman", "FASTAPI_URL")
POSTMAN_API_KEY = config.get("postman", "POSTMAN_API_KEY")
WORKSPACE_ID = config.get("postman", "WORKSPACE_ID")

router = APIRouter()


@router.get("/sync", response_model=SuccessResponseDto)
def sync(payload: dict = Depends(get_user_or_error) , Authorization: Annotated[str | None, Header()] = None):

    try:
        header = {
            'Authorization' : Authorization
        }
        res = requests.get(FASTAPI_URL , headers=header)
        res.raise_for_status()
        openapi_res = res.text  # OpenAPI JSON string
        get_collections_url = "https://api.getpostman.com/collections"
        headers = {"X-Api-Key": POSTMAN_API_KEY, "Content-Type": "application/json"}

        collections_res = requests.get(url=get_collections_url, headers=headers)
        collections_res.raise_for_status()
        collections = collections_res.json().get("collections", [])

        for collection in collections:
            collection_id = collection.get("id")
            delete_url = f"https://api.getpostman.com/collections/{collection_id}"
            delete_res = requests.delete(delete_url, headers=headers)
            print(f"Deleted {collection['name']}: {delete_res.status_code}")

        import_url = (
            f"https://api.getpostman.com/import/openapi?workspace={WORKSPACE_ID}"
        )
        import_payload = {"type": "string", "input": openapi_res}

        import_res = requests.post(import_url, headers=headers, json=import_payload)
        import_res.raise_for_status()

        return {
            "message": "درخواست انجام شد",
            "data": {
                "stdout": import_res.json(),
                "stderr": None,
            },
        }

    except requests.exceptions.RequestException as e:
        print(e)

        return {}
        # raise HTTPException(status_code=500, detail=str(e))
