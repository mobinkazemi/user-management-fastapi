from fastapi import APIRouter, Depends, HTTPException, Request
from auth.functions.get_user_or_error import get_user_or_error
from shared.dto.response.api_responseDto import SuccessResponseDto
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/postman", response_model=SuccessResponseDto)
def postman():
    return RedirectResponse("http://localhost:8000/openapi.json")
