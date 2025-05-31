from fastapi import APIRouter, Depends, HTTPException
from auth.functions.get_user_or_error import get_user_or_error
from shared.dto.response.api_responseDto import SuccessResponseDto
from roles.repository import RoleRepository
from users.repository import UserRepository
from userRole.repository import UserRoleRepository
from userRole.dto.request.apply_user_role_changes import ApplyUserRoleChangesDto
from shared.classes.User_Session_Manager import UserSessionManager as USManager

router = APIRouter()
roleRepo = RoleRepository()
userRepo = UserRepository()
userRoleRepo = UserRoleRepository()
userSession = USManager()


@router.post("/add", response_model=SuccessResponseDto)
def addRole(data: ApplyUserRoleChangesDto, payload: dict = Depends(get_user_or_error)):
    user = userRepo.findById(data.userId)
    role = roleRepo.findById(data.roleId)

    dict_data = data.model_dump()

    record = userRoleRepo.findOne(
        userId=dict_data.get("userId"), roleId=dict_data.get("roleId")
    )

    if not user:
        raise HTTPException(404, detail="کاربر پیدا نشد")

    if not role:
        raise HTTPException(404, detail="نقش پیدا نشد")

    if record:
        raise HTTPException(400, detail="رکورد نقش کاربر قبلاً وجود دارد")

    previousRole = userRoleRepo.findOne(userId=dict_data.get("userId"))

    global message

    if previousRole:
        userRoleRepo.updateOne(previousRole.get("id"), {"roleId": data.roleId})
        message = f"نقش کاربر با موفقیت به {role['name']} تغییر کرد"

    else:
        data = dict({"userId": data.userId, "roleId": data.roleId})

        result = userRoleRepo.createOne(data)

        userRepo.updateOne(user.get("id"), dict({"userRoleId": result.get("id")}))

        message = f"تعریف نقش {role['name']} برای کاربر انجام شد"

    if userSession.hasSession(dict_data.get("userId")):
        userSession.logout(dict_data.get("userId"))

    return {"data": {}, "message": message}


@router.delete("/remove", response_model=SuccessResponseDto)
def removeRole(
    data: ApplyUserRoleChangesDto, payload: dict = Depends(get_user_or_error)
):
    user = userRepo.findById(data.userId)
    role = roleRepo.findById(data.roleId)

    dict_data = data.model_dump()

    record = userRoleRepo.findOne(
        userId=dict_data.get("userId"), roleId=dict_data.get("roleId")
    )

    if not user:
        raise HTTPException(404, detail="کاربر پیدا نشد")

    if not role:
        raise HTTPException(404, detail="نقش پیدا نشد")

    if not record:
        raise HTTPException(404, detail="رکورد نقش کاربر پیدا نشد")

    userRoleRepo.deleteOne(record["id"])

    userRepo.updateOne(user.get("id"), dict({"userRoleId": None}))

    if userSession.hasSession(dict_data.get("userId")):
        userSession.logout(dict_data.get("userId"))

    return {"data": {}, "message": "نقش با موفقیت از کاربر حذف شد"}
