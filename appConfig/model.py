from sqlalchemy import Column, Integer
from db.database import Base, engine
from shared.models.base_model import BaseDBModel


class AppConfig(Base, BaseDBModel):
    __tablename__ = "appConfig"

    id = Column(Integer, primary_key=True, index=True)
    expirePasswordDays = Column(Integer, nullable=True, default=90)
    passwordAdvantageDays = Column(Integer, nullable=True, default=3)

    def __init__(self, data):
        data = dict(data)
        self.expirePasswordDays = data.get("expirePasswordDays")
        self.passwordAdvantageDays = data.get("passwordAdvantageDays")


Base.metadata.create_all(engine)
