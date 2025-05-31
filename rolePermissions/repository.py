from shared.repository.baseRepository import BaseRepository
from . import model
from db.database import session
from roles.dto.request.create_role_dto import CreateRoleDto
from sqlalchemy import select
from roles.model import Role
from permissions.model import Permission


class RolePermissionRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model.RolePermission)

    def findRolesByPermissionId(self, permission_id: int):
        stmt = (
            select(Role)
            .join(model.RolePermission, Role.id == model.RolePermission.role_id)
            .where(model.RolePermission.permission_id == permission_id)
        )
        result = self.session.execute(stmt).scalars().all()

        result = [r.__dict__ for r in result]

        for r in result:
            r.pop("_sa_instance_state", None)

        return result

    def findPermissionsByRoleId(self, role_id: int):
        stmt = (
            select(Permission)
            .join(
                model.RolePermission,
                Permission.id == model.RolePermission.permission_id,
            )
            .where(model.RolePermission.role_id == role_id)
        )
        result = self.session.execute(stmt).scalars().all()

        result = [r.__dict__ for r in result]

        for r in result:
            r.pop("_sa_instance_state", None)

        return result
