from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import List, Optional
import re


class RegisterDto(BaseModel):
    firstName: str = Field(min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$")
    lastName: str = Field(min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$")
    nationalId: str = Field(min_length=5, max_length=10, pattern=r"^[0-9]+$")
    gender: int = Field(ge=1, le=2)
    education: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")

    password: str = Field(min_length=8, max_length=128)
    passwordHistoryCount: Optional[int] = Field(default=None, ge=0)
    expirePasswordDays: Optional[int] = Field(default=None, ge=0)
    mustChangePassword: Optional[bool] = Field(default=True)
    passwordAdvantageDays: Optional[int] = Field(default=None, ge=0)

    active: Optional[bool] = Field(default=True)
    # deactivedAt: Optional[date] = Field(default=None)

    email: EmailStr = Field(
        ...,
        max_length=250,
    )
    cellphone: str = Field(
        ..., pattern=r"^(?:(?:(?:\\+?|00)(98))|(0))?((?:90|91|92|93|99)[0-9]{8})$"
    )
    profileId: int = Field(..., ge=1)
    userFileIds: List[int] = Field(default_factory=list, min=0)

    #
    # @field_validator("password")
    # def validate_password(cls, value):
    #     # Check for at least one uppercase, lowercase, number, and special character
    #     if not re.match(
    #         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", value
    #     ):
    #         raise ValueError(
    #             "رمز عبور باید شامل حروف بزرگ، حروف کوچک، اعداد و کاراکتر های خاص (@,!#$% و ...) باشد"
    #         )
    #     return value

    @field_validator("userFileIds")
    def validate_userFileIds(cls, value):
        # Ensure all file IDs are positive
        if any(file_id <= 0 for file_id in value):
            raise ValueError("همه شناسه های فایل باید اعداد صحیح مثبت باشند")
        return value
