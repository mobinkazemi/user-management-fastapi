from fastapi import APIRouter, Depends, HTTPException
from auth.functions.get_user_or_error import get_user_or_error
from shared.dto.response.api_responseDto import SuccessResponseDto
from roles.repository import RoleRepository
from permissions.repository import PermissionRepository
from rolePermissions.repository import RolePermissionRepository
from permissionsCategory.repository import PermissionCategoryRepository

router = APIRouter()
roleRepo = RoleRepository()
permissionRepo = PermissionRepository()
rolePermissionRepo = RolePermissionRepository()
permissionCategoryRepo = PermissionCategoryRepository()


@router.get("/listByCategory/{category_id}", response_model=SuccessResponseDto)
def get_permissions_of_one_role(
    category_id: int, payload: dict = Depends(get_user_or_error)
):
    result = []

    result = permissionRepo.get_filtered_permissions_grouped_with_category(category_id)

    return {"data": result}


@router.get("/listByCategory", response_model=SuccessResponseDto)
def get_permissions_of_one_role(payload: dict = Depends(get_user_or_error)):
    result = []

    result = permissionRepo.get_all_permissions_grouped_with_category()

    return {"data": result}
