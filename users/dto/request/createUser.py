from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class CreateUserDto(BaseModel):
    name: str
    username: str | None = None
    password: str | None = None
