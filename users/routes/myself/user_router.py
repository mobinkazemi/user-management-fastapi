from fastapi import APIRouter, Depends, HTTPException
from shared.dto.response.api_responseDto import SuccessResponseDto
from auth.functions.get_user_or_error import get_user_or_error
from users.repository import UserRepository
from users.dto.request.myself.changePassword import ChangePasswordByMyself
from shared.classes.password_manager import PasswordManager as PW
from auth.classes.twp_fa_manager import TwoFactorAuthManager as TFAManager
from users.dto.request.myself.verfiyActivate2Fa import VerifyActivate2FADto

router = APIRouter()
userRepo = UserRepository()
passwordManager = PW()


@router.post("/changePassword", response_model=SuccessResponseDto)
def change_password_by_myself(
    data: ChangePasswordByMyself, payload: dict = Depends(get_user_or_error)
):
    userId = payload.get("id")
    data: dict = dict(data)

    user = userRepo.findById(userId)

    if user is None:
        raise HTTPException(400, detail="کاربر پیدا نشد")

    currentPassword = data.get("password")

    if passwordManager.verify(currentPassword, user["password"]) is False:
        raise HTTPException(400, detail="رمز عبور فعلی اشتباه است")

    # check with password history manager
    passwordManager.sync_history(dict(user), data.get("newPassword"))

    passwordManager.change(userId, data.get("newPassword"))

    return {}


@router.post("/requestActivate2FA", response_model=SuccessResponseDto)
def request_activate_2fa(payload: dict = Depends(get_user_or_error)):
    userId = payload.get("id")

    user = userRepo.findById(userId)

    if user is None:
        raise HTTPException(400, detail="کاربر پیدا نشد")

    if user["twoFAEnabled"]:
        raise HTTPException(400, detail="احراز هویت دو مرحله ای قبلا فعال شده است")

    if not user["cellphone"]:
        raise HTTPException(400, detail="شماره همراه شما ثبت نشده است")

    twoFactorAuthManager = TFAManager()
    twoFactorAuthManager.setActivate2FAOtp(userId, user["cellphone"])

    return {
        "data": {},
        "message": "کد تایید جهت فعال سازی احراز هویت دو مرحله ای به شماره همراه شما ارسال شد",
    }


@router.post("/VerifyActivate2FA", response_model=SuccessResponseDto)
def verify_activate_2fa(
    data: VerifyActivate2FADto, payload: dict = Depends(get_user_or_error)
):
    data: dict = dict(data)
    userId = payload.get("id")

    user = userRepo.findById(userId)

    if user is None:
        raise HTTPException(400, detail="کاربر پیدا نشد")

    twoFactorAuthManager = TFAManager()
    result = twoFactorAuthManager.verifyActivate2FA(userId, data["otp"])

    if not result:
        raise HTTPException(400, detail="کد تایید اشتباه است")

    userRepo.updateOne(userId, {"twoFAEnabled": True})

    return {
        "data": {},
        "message": "احراز هویت دو مرحله ای با موفقیت فعال شد",
    }
