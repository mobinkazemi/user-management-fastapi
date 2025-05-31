from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class UpdateRoleDto(BaseModel):
    name: str
    id: int
