from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class VerifyOtpDto(BaseModel):
    username: str
    otp: str
