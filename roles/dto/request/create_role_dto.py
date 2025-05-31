from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class CreateRoleDto(BaseModel):
    name: str

