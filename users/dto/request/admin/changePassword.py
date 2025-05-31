from pydantic import BaseModel, Field, field_validator
import re


class ChangePasswordByAdmin(BaseModel):
    userId: int = Field(min=1)
    password: str = Field(min_length=8, max_length=128)
    newPassword: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, value):
        # Check for at least one uppercase, lowercase, number, and special character
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", value
        ):
            raise ValueError(
                "رمز عبور باید شامل حروف بزرگ، حروف کوچک، اعداد و کاراکتر های خاص (@,!#$% و ...) باشد"
            )
        return value

    @field_validator("newPassword")
    def validate_password_new(cls, value):
        # Check for at least one uppercase, lowercase, number, and special character
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", value
        ):
            raise ValueError(
                "رمز عبور باید شامل حروف بزرگ، حروف کوچک، اعداد و کاراکتر های خاص (@,!#$% و ...) باشد"
            )
        return value
