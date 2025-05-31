from sqlalchemy import (
    Column,
    Integer,
    String,
    SMALLINT,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY
from db.database import Base, engine
from shared.models.base_model import BaseDBModel
from users.dto.request.createUser import CreateUserDto
from userRole.model import UserRole


class User(Base, BaseDBModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    nationalId = Column(String, nullable=True)
    # gender: 1: male, 2: female
    gender = Column(SMALLINT, nullable=True)
    education = Column(String, nullable=True)
    username = Column(String, nullable=False)

    # password fields
    password = Column(String, nullable=False)
    passwordHistoryCount = Column(SMALLINT, nullable=True, default=3)
    passwordHistories = Column(ARRAY(String), nullable=True, default=[])
    expirePasswordDays = Column(
        Integer,
        nullable=True,
    )
    mustChangePassword = Column(Boolean, nullable=True, default=True)
    passwordAdvantageDays = Column(
        SMALLINT,
        nullable=True,
    )
    passwordChangedAt = Column(TIMESTAMP, nullable=True, default=func.now())
    ###################################################################

    userRoleId = Column(Integer, ForeignKey(UserRole.id), nullable=True)
    active = Column(Boolean, nullable=True, default=True)
    deactivedAt = Column(TIMESTAMP, nullable=True)

    email = Column(String, nullable=True)
    cellphone = Column(String, nullable=True)
    twoFAEnabled = Column(Boolean, nullable=True, default=False)
    profileId = Column(Integer, nullable=True)
    userFileIds = Column(ARRAY(Integer), nullable=True, default=[])
    lastSessionDate = Column(TIMESTAMP, nullable=True)
    isSuperAdmin = Column(Boolean, nullable=False, default=False)

    def __init__(self, data):
        data: dict = dict(data)
        self.firstName = data.get("firstName")
        self.lastName = data.get("lastName")
        self.nationalId = data.get("nationalId")
        self.gender = data.get("gender")
        self.education = data.get("education")
        self.username = data.get("username")
        self.password = data.get("password")
        self.passwordHistoryCount = data.get("passwordHistoryCount")
        self.passwordHistories = data.get("passwordHistories")
        self.mustChangePassword = data.get("mustChangePassword")
        self.passwordAdvantageDays = data.get("passwordAdvantageDays")
        self.userRoleId = data.get("userRoleId")
        self.active = data.get("active")
        self.email = data.get("email")
        self.cellphone = data.get("cellphone")
        self.twoFAEnabled = data.get("twoFAEnabled")
        self.profileId = data.get("profileId")
        self.userFileIds = data.get("userFileIds")
        self.lastSessionDate = data.get("lastSessionDate")
        self.deactivedAt = data.get("deactivedAt")
        self.passwordChangedAt = data.get("passwordChangedAt")
        self.isSuperAdmin = data.get("isSuperAdmin", False)

Base.metadata.create_all(engine)
