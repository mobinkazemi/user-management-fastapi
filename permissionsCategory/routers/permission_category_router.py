from fastapi import APIRouter, Depends, HTTPException, Request
from auth.functions.get_user_or_error import get_user_or_error
from shared.dto.response.api_responseDto import SuccessResponseDto
from permissionsCategory.repository import PermissionCategoryRepository

router = APIRouter()
permissionCategoryRepo = PermissionCategoryRepository()


@router.get("/list", response_model=SuccessResponseDto)
def list(payload: dict = Depends(get_user_or_error)):
    permissionCategoryList = permissionCategoryRepo.findAll()

    return {"data": permissionCategoryList}
