from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class DeleteUserRoleDto(BaseModel):
    userId: int
    roleId: int
