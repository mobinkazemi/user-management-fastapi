from fastapi import APIRouter, Depends, HTTPException
from auth.functions.get_user_or_error import get_user_or_error
from shared.dto.response.api_responseDto import SuccessResponseDto
from roles.repository import RoleRepository
from roles.dto.request.update_role_dto import UpdateRoleDto

router = APIRouter()
roleRepo = RoleRepository()


@router.get("/list", response_model=SuccessResponseDto)
def listRoles(payload: dict = Depends(get_user_or_error)):
    roles = roleRepo.findAll()
    return {"data": roles}


@router.patch("/update", response_model=SuccessResponseDto)
def updateRole(data: UpdateRoleDto, payload: dict = Depends(get_user_or_error)):
    role_exists = roleRepo.findById(data.id)

    if not role_exists:
        raise HTTPException(404, detail="نقش پیدا نشد")

    result = roleRepo.updateOne(data.id, dict(data))

    if result:
        return {"data": result}

    raise HTTPException(400, "خطایی در فرایند ویرایش نقش رخ داده است")
