from fastapi import APIRouter, Depends, HTTPException
from auth.functions.get_user_or_error import get_user_or_error
from shared.dto.response.api_responseDto import SuccessResponseDto
from roles.repository import RoleRepository
from permissions.repository import PermissionRepository
from rolePermissions.repository import RolePermissionRepository
from rolePermissions.dto.AddPermissionsToRolesDto import AddPermissionsToRolesDto
from permissionsCategory.repository import PermissionCategoryRepository
from rolePermissions.functions.check_role_and_permission_ids import (
    check_role_and_permission_ids,
)
from rolePermissions.functions.create_role_permission_pairs import (
    create_role_permission_pairs,
)

router = APIRouter()

roleRepo = RoleRepository()
permissionRepo = PermissionRepository()
rolePermissionRepo = RolePermissionRepository()
permissionCategoryRepo = PermissionCategoryRepository()


@router.post("/add", response_model=SuccessResponseDto)
def add_permissions_to_roles(
    data: AddPermissionsToRolesDto, payload: dict = Depends(get_user_or_error)
):
    check_role_and_permission_ids(data)

    pairs = create_role_permission_pairs(data)

    for pair in pairs:
        if rolePermissionRepo.findOne(
            role_id=pair["role_id"], permission_id=pair["permission_id"]
        ):
            continue
        rolePermissionRepo.createOne(pair)

    return {"message": "دسترسی ها با موفقیت اضافه شد"}


@router.delete("/remove", response_model=SuccessResponseDto)
def remove_permissions_from_roles(
    data: AddPermissionsToRolesDto, payload: dict = Depends(get_user_or_error)
):
    check_role_and_permission_ids(data)

    pairs = create_role_permission_pairs(data)

    for pair in pairs:
        item = rolePermissionRepo.findOne(
            role_id=pair["role_id"], permission_id=pair["permission_id"]
        )
        if not item:
            continue
        rolePermissionRepo.deleteOne(item["id"])

    return {"message": "دسترسی ها با موفقیت حذف شد"}


@router.get("/rolesOfPermission/{permission_id}", response_model=SuccessResponseDto)
def get_roles_of_one_permission(
    permission_id: int, payload: dict = Depends(get_user_or_error)
):

    permission = permissionRepo.findById(permission_id)

    if not permission:
        raise HTTPException(404, "دسترسی پیدا نشد")

    result = rolePermissionRepo.findRolesByPermissionId(permission_id=permission_id)

    return {"data": result}


@router.get("/permissionsOfRole/{role_id}", response_model=SuccessResponseDto)
def get_permissions_of_one_role(
    role_id: int, payload: dict = Depends(get_user_or_error)
):

    role = roleRepo.findById(role_id)

    if not role:
        raise HTTPException(404, "نقش پیدا نشد")

    result = rolePermissionRepo.findPermissionsByRoleId(role_id=role_id)

    return {"data": result}
