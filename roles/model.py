from sqlalchemy import Column, Integer, String , Boolean , ARRAY
from db.database import Base, engine
from shared.models.base_model import BaseDBModel
from roles.dto.request.create_role_dto import CreateRoleDto


class Role(Base, BaseDBModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    maxRequestPerMinute = Column(Integer ,default=120 , nullable=True )
    active  = Column(Boolean , default=True , nullable=False)
    workingDayLimit = Column(ARRAY(Integer) , nullable= True)
    workingTimeLimit = Column(String , nullable= False)
    def __init__(self, data: CreateRoleDto):
        data = dict(data)
        self.name = data.get("name")
        self.maxRequestPerMinute = data.get("maxRequestPerMinute")
        self.active = data.get("active", True)
        self.workingDayLimit = data.get("workingDayLimit")
        self.workingTimeLimit = data.get("workingTimeLimit")


Base.metadata.create_all(engine)
