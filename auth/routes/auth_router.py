from fastapi import APIRouter, HTTPException, Depends
from auth.dto.request.login import LoginDto
from auth.dto.request.register import RegisterDto
from auth.functions.create_token import create_access_token
from shared.dto.response.api_responseDto import SuccessResponseDto
from users.repository import UserRepository
import datetime
from userConfig.repository import UserConfigRepository
from shared.classes.password_manager import PasswordManager as PW
from shared.classes.User_Session_Manager import UserSessionManager as USManager
from auth.functions.get_user_or_error import get_user_or_error
from auth.classes.twp_fa_manager import TwoFactorAuthManager as TFAManager
from auth.dto.request.verify_otp import VerifyOtpDto
from auth.functions.login_handler import finalizeLogin

router = APIRouter()
userRepo = UserRepository()
userConfigRepo = UserConfigRepository()
passwordManager = PW()
userSessionManager = USManager()


@router.post("/login", response_model=SuccessResponseDto)
def login(data: LoginDto):
    data: dict = dict(data)

    user = userRepo.findByUsername(data.get("username"))

    if user is None:
        raise HTTPException(400, detail="نام کاربری یا رمز عبور اشتباه است")

    if passwordManager.verify(data.get("password"), user["password"]) is False:
        raise HTTPException(400, detail="نام کاربری یا رمز عبور اشتباه است")

    if passwordManager.hadExpired(user):
        raise HTTPException(403, "گذرواژه شما منقضی شده است")
    # check password expiration

    if user["active"] is False:
        raise HTTPException(400, "کاربر غیر فعال است")

    if user["twoFAEnabled"]:
        twoFactorAuthManager = TFAManager()
        twoFactorAuthManager.setOtp(user["id"], user["cellphone"])

        return {
            "data": {},
            "message": "کد تایید ۲ مرحله ای به شماره همراه شما ارسال شد",
        }

    if not user["userRoleId"]:
        raise HTTPException(401, "نقش شما هنوز مشخص نشده است")

    loginResult = finalizeLogin(user)

    return {
        "data": {"token": loginResult["token"], "user": loginResult["user"]},
        "message": "ورود با موفقیت انجام شد",
    }


@router.post("/register", response_model=SuccessResponseDto)
def register(data: RegisterDto):
    data: dict = dict(data)
    user = userRepo.findByUsername(data.get("username"))

    if user:
        raise HTTPException(400, detail="نام کاربری تکراری است")

    if len(data.get("password")) < 4:
        raise HTTPException(400, detail="رمز عبور باید حداقل 4 کاراکتر باشد")

    plaintext_password = data.get("password")
    hashed_password = passwordManager.hash(data["password"])

    data["password"] = hashed_password

    data["mustChangePassword"] = False

    user = userRepo.createOne(data)

    passwordManager.sync_history(user, plaintext_password)

    del user["password"]
    del user["passwordHistories"]
    del user["passwordHistoryCount"]

    return {
        "data": user,
        "message": "ثبت نام با موفقیت انجام شد",
    }


@router.post("/logout", response_model=SuccessResponseDto)
def logout(payload: dict = Depends(get_user_or_error)):
    userId = payload.get("id")

    # حذف سشن کاربر
    userSessionManager.logout(userId)

    return {}


@router.post("/verifyOtp", response_model=SuccessResponseDto)
def verify_otp(data: VerifyOtpDto):
    data: dict = dict(data)

    user = userRepo.findByUsername(data.get("username"))

    if user is None:
        raise HTTPException(400, detail="نام کاربری یا رمز عبور اشتباه است")

    if not user["twoFAEnabled"]:
        raise HTTPException(400, "ورود ۲ مرحله ای برای شما فعال نیست")

    twoFactorAuthManager = TFAManager()
    if twoFactorAuthManager.verifyOtp(user["id"], data.get("otp")) is False:
        raise HTTPException(400, detail="کد تایید اشتباه است")

    loginResult = finalizeLogin(user)

    return {
        "data": {"token": loginResult["token"], "user": loginResult["user"]},
        "message": "ورود با موفقیت انجام شد",
    }
