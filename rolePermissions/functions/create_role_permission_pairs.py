from rolePermissions.dto.AddPermissionsToRolesDto import AddPermissionsToRolesDto
from permissions.repository import PermissionRepository
from fastapi import HTTPException

permissionRepo = PermissionRepository()


def create_role_permission_pairs(data: AddPermissionsToRolesDto):
    pairs = []

    if data.role_ids and data.permission_ids:
        for r in data.role_ids:
            for p in data.permission_ids:
                pairs.append({"role_id": r, "permission_id": p})

    elif data.role_ids and data.permission_category_ids:
        for cp in data.permission_category_ids:
            permissions = permissionRepo.findAllAndFilter(category_id=cp)
            for p in permissions:
                for r in data.role_ids:
                    pairs.append({"role_id": r, "permission_id": p["id"]})

    else:
        raise HTTPException(400, detail="دیتای ورودی معتبر نیست")

    return pairs
