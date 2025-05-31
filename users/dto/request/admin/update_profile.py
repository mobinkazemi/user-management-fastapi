from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import List, Optional
import re

class UpdateUserProfileByAdminDto(BaseModel):
    userId: int = Field(min=1)
    firstName: Optional[str] = Field(default=None)
    lastName: Optional[str] = Field(default=None)
    nationalId: Optional[str] = Field(default=None)
    gender: Optional[int] = Field(default=None, ge=1, le=2)
    education: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    passwordHistoryCount: Optional[int] = Field(default=None, ge=1, le=10)
    mustChangePassword: Optional[bool] = Field(default=None)
    passwordAdvantageDays: Optional[int] = Field(default=None, ge=1, le=10)
    active: Optional[bool] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    cellphone: Optional[str] = Field(default=None)
    twoFAEnabled: Optional[bool] = Field(default=None)
    profileId: Optional[int] = Field(default=None, ge=1)
    userFileIds: Optional[List[int]] = Field(default=None, ge=1)
    deactivedAt: Optional[date] = Field(default=None)

    @field_validator("username")
    def validate_username(cls, value):
        if value and not value.isalnum():
            raise ValueError("نام کاربری باید فقط شامل حروف و اعداد باشد")
        return value
    
    @field_validator("nationalId")
    def validate_national_id(cls, value):
        if value and not value.isdigit():
            raise ValueError("کد ملی باید فقط شامل اعداد باشد")
        return value
    
    @field_validator("cellphone")
    def validate_cellphone(cls, value):
        if value and not re.match(r"^(\+98|0)?9\d{9}$", value):
            raise ValueError("شماره تلفن همراه باید با 09 شروع شود و 11 رقم باشد")
        return value
    
    @field_validator("email")
    def validate_email(cls, value):
        if value and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("ایمیل باید یک آدرس ایمیل معتبر باشد")
        return value

    @field_validator("profileId")
    def validate_profile_id(cls, value):
        if value and value < 1:
            raise ValueError("شناسه پروفایل باید بزرگتر از 0 باشد")
        return value
    
    @field_validator("userFileIds", mode="before")
    def validate_user_file_ids(cls, value):
        if value is not None and not all(isinstance(i, int) and i > 0 for i in value):
            raise ValueError("شناسه فایل های کاربر باید لیستی از اعداد صحیح مثبت باشد")
        return value
    @field_validator("passwordHistoryCount")
    def validate_password_history_count(cls, value):
        if value and (value < 1 or value > 10):
            raise ValueError("تعداد تاریخچه رمز عبور باید بین 1 تا 10 باشد")
        return value
    
    @field_validator("passwordAdvantageDays")
    def validate_password_advantage_days(cls, value):
        if value and (value < 1 or value > 10):
            raise ValueError("روزهای مزیت رمز عبور باید بین 1 تا 10 باشد")
        return value
    
    @field_validator("mustChangePassword" , "active" , "twoFAEnabled")
    def validate_must_change_password(cls, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("باید تغییر رمز عبور یک مقدار بولی باشد")
        return value
     
    @field_validator("firstName", "lastName")
    def validate_name(cls, value):
        if value and not value.isalpha():
            raise ValueError("نام و نام خانوادگی باید فقط شامل حروف باشد")
        return value
    
    @field_validator("education")
    def validate_education(cls, value):
        educationDict = [
            "سیکل",
            "پیش دانشگاهی",
            "دیپلم",
            "فوق دیپلم",
            "لیسانس",
            "فوق لیسانس",
            "دکتری",
            "بیسواد"
        ]
        if value and value not in educationDict:
            raise ValueError(f"تحصیلات باید یکی از مقادیر زیر باشد: {', '.join(educationDict)}")
        return value
    
    @field_validator("gender")
    def validate_gender(cls, value):
        if value and value not in [1, 2]:
            raise ValueError("جنسیت باید 1 (مرد) یا 2 (زن) باشد")
        return value
    
    @field_validator("deactivedAt" )
    def validate_deactived_at(cls, value):
        if value and not isinstance(value, date):
            raise ValueError("تاریخ غیرفعال شدن باید یک تاریخ معتبر باشد")
        return value
    



    