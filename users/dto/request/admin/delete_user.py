from pydantic import BaseModel, Field


class DeleteUserByAdminDto(BaseModel):
    userId: int = Field(min=1)
