from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class ApplyUserRoleChangesDto(BaseModel):
    userId: int
    roleId: int
