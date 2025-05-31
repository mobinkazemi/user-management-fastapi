from fastapi import HTTPException
from rolePermissions.dto.AddPermissionsToRolesDto import AddPermissionsToRolesDto
from roles.repository import RoleRepository
from permissions.repository import PermissionRepository
from permissionsCategory.repository import PermissionCategoryRepository


roleRepo = RoleRepository()
permissionRepo = PermissionRepository()
permissionCategoryRepo = PermissionCategoryRepository()


def check_role_and_permission_ids(data: AddPermissionsToRolesDto):
    if data.role_ids:
        for role_id in data.role_ids:
            this_role_exists = roleRepo.findById(role_id)
            if not this_role_exists:
                raise HTTPException(404, detail="نقش موجود نیست")

    if data.permission_ids:
        for permission_id in data.permission_ids:
            this_permission_exists = permissionRepo.findById(permission_id)
            if not this_permission_exists:
                raise HTTPException(404, detail="دسترسی موجود نیست")

    if data.permission_category_ids:
        for permission_category_id in data.permission_category_ids:
            this_permission_category_exists = permissionCategoryRepo.findById(
                permission_category_id
            )
            if not this_permission_category_exists:
                raise HTTPException(404, detail="گروه دسترسی موجود نیست")
