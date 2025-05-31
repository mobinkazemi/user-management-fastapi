from pydantic import BaseModel


class VerifyActivate2FADto(BaseModel):
    otp: str
