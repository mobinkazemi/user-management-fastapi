from sqlalchemy import Column, Integer, String
from db.database import Base, engine
from shared.models.base_model import BaseDBModel
from roles.dto.request.create_role_dto import CreateRoleDto
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class PermissionCategory(Base, BaseDBModel):
    __tablename__ = "permission_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    ref = Column(String, nullable=True)

    permissions = relationship("Permission", back_populates="category")

    def __init__(self, data):
        data = dict(data)
        self.name = data.get("name", None)
        self.ref = data.get("ref", None)


Base.metadata.create_all(engine)
