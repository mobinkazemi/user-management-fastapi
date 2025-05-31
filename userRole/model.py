from sqlalchemy import Column, Integer
from db.database import Base, engine
from shared.models.base_model import BaseDBModel
from userRole.dto.request.apply_user_role_changes import ApplyUserRoleChangesDto


class UserRole(Base, BaseDBModel):
    __tablename__ = "userRoles"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, nullable=False)
    roleId = Column(Integer, nullable=False)

    def __init__(self, data: ApplyUserRoleChangesDto):
        try:
            self.userId = data.userId
            self.roleId = data.roleId
        except AttributeError as e:
            self.userId = data["userId"]
            self.roleId = data["roleId"]


Base.metadata.create_all(engine)
