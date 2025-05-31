from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base, engine
from shared.models.base_model import BaseDBModel
from roles.dto.request.create_role_dto import CreateRoleDto
from roles.model import Role
from permissions.model import Permission


class RolePermission(Base, BaseDBModel):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(ForeignKey(Role.id), nullable=False)
    permission_id = Column(ForeignKey(Permission.id), nullable=False)

    def __init__(self, data):
        data = dict(data)
        self.role_id = data.get("role_id")
        self.permission_id = data.get("permission_id")


Base.metadata.create_all(engine)
