from fastapi import APIRouter, Depends, HTTPException
from shared.dto.response.api_responseDto import SuccessResponseDto
from auth.functions.get_user_or_error import get_user_or_error
from users.repository import UserRepository
from users.dto.request.admin.changePassword import ChangePasswordByAdmin
from shared.classes.password_manager import PasswordManager as PW
from users.dto.request.admin.update_profile import UpdateUserProfileByAdminDto
from users.dto.request.admin.delete_user import DeleteUserByAdminDto

import datetime

router = APIRouter()
userRepo = UserRepository()
passwordManager = PW()


@router.post("/changePassword", response_model=SuccessResponseDto)
def change_password_by_admin(
    data: ChangePasswordByAdmin, payload: dict = Depends(get_user_or_error)
):
    data: dict = dict(data)

    userId = data.get("userId")

    user = userRepo.findById(userId)

    if user is None:
        raise HTTPException(400, detail="کاربر پیدا نشد")

    currentPassword = data.get("password")

    if passwordManager.verify(currentPassword, user["password"]) is False:
        raise HTTPException(400, detail="رمز عبور فعلی اشتباه است")

    newPasswordHashed = passwordManager.hash(data.get("newPassword"))

    # check with password history manager
    passwordManager.sync_history(user, data.get("newPassword"))

    passwordManager.change(userId, data.get("newPassword"))

    return {}


@router.get("/list", response_model=SuccessResponseDto)
def list_users(payload: dict = Depends(get_user_or_error)):
    users = userRepo.findAll()

    for u in users:
        del u["password"]
        del u["passwordChangedAt"]
        del u["passwordHistories"]

    return {"data": users, "message": "لیست کاربران دریافت شد"}


@router.get("/info/{userId}", response_model=SuccessResponseDto)
def get_user_info(userId: int, payload: dict = Depends(get_user_or_error)):
    user = userRepo.findById(userId)

    if not user:
        raise HTTPException(404, detail="کاربر پیدا نشد")

    del user["password"]
    del user["passwordChangedAt"]
    del user["passwordHistories"]

    return {"data": user, "message": "اطلاعات کاربر دریافت شد"}


@router.patch("/update", response_model=SuccessResponseDto)
def update_user_by_admin(
    data: UpdateUserProfileByAdminDto, payload: dict = Depends(get_user_or_error)
):
    data = dict(data)
    updateData = dict({})

    user = userRepo.findOne(id=data["userId"])

    if data["firstName"]:
        updateData["firstName"] = data["firstName"]
    #################
    if data["lastName"]:
        updateData["lastName"] = data["lastName"]
    #################
    if data["nationalId"]:
        updateData["nationalId"] = data["nationalId"]
    #################
    if data["gender"]:
        updateData["gender"] = data["gender"]
    #################
    if data["education"]:
        updateData["education"] = data["education"]
    #################
    if data["username"]:
        duplicate = userRepo.findOne(username=data["username"])
        if duplicate and duplicate["id"] != data["userId"]:
            raise HTTPException(403, "نام کاربری قبلا تعریف شده است")
        updateData["username"] = data["username"]
    #################
    if data["passwordHistoryCount"]:
        updateData["passwordHistoryCount"] = data["passwordHistoryCount"]
        if data["passwordHistoryCount"] < user["passwordHistoryCount"]:
            while len(user["passwordHistories"]) > data["passwordHistoryCount"]:
                user["passwordHistories"].pop(0)
            userRepo.updateOne(
                user["id"], {"passwordHistories": user["passwordHistories"]}
            )
    #################
    if data["mustChangePassword"]:
        updateData["mustChangePassword"] = data["mustChangePassword"]
    #################
    if data["passwordAdvantageDays"]:
        updateData["passwordAdvantageDays"] = data["passwordAdvantageDays"]
    #################
    if data["active"]:
        updateData["active"] = data["active"]
    #################
    if data["email"]:
        updateData["email"] = data["email"]
    #################
    if data["cellphone"]:
        updateData["cellphone"] = data["cellphone"]
    #################
    if data["twoFAEnabled"]:
        updateData["twoFAEnabled"] = data["twoFAEnabled"]
    #################
    if data["profileId"]:
        updateData["profileId"] = data["profileId"]
    #################
    if data["userFileIds"]:
        updateData["userFileIds"] = data["userFileIds"]
    #################
    if data["deactivedAt"]:
        updateData["deactivedAt"] = data["deactivedAt"]

    userRepo.updateOne(data["userId"], updateData)

    return {}


@router.delete("/delete", response_model=SuccessResponseDto)
def delete_user_by_admin(
    data: DeleteUserByAdminDto, payload: dict = Depends(get_user_or_error)
):
    data = dict(data)
    user = userRepo.findOne(id=data["userId"])

    if not user:
        raise HTTPException(404, detail="کاربر پیدا نشد")

    userRepo.deleteOne(user["id"])

    return {}
