from sqlalchemy import String, ForeignKey, Integer, Column
from db.database import Base, engine
from shared.models.base_model import BaseDBModel
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import TYPE_CHECKING, List


class Permission(Base, BaseDBModel):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, nullable=False)
    url = Column(String, nullable=False)
    text = Column(String, nullable=True)
    category_id = Column(ForeignKey("permission_category.id"), nullable=False)

    category = relationship("PermissionCategory", back_populates="permissions")

    def __init__(self, data):
        data = dict(data)
        self.method = data.get("method", None)
        self.url = data.get("url", None)
        self.text = data.get("text", None)
        self.category_id = data.get("category_id", None)


Base.metadata.create_all(engine)
