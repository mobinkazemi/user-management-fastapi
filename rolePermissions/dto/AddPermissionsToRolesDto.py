from typing import List, Optional
from pydantic import BaseModel


class AddPermissionsToRolesDto(BaseModel):
    permission_ids: Optional[List[int]] = None
    role_ids: List[int]
    permission_category_ids: Optional[List[int]] = None
