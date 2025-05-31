from fastapi import HTTPException
from users.repository import UserRepository
from passlib.hash import pbkdf2_sha256
from passlib.hash import pbkdf2_sha256
from userConfig.repository import UserConfigRepository

from datetime import datetime, timezone, timedelta


userRepo = UserRepository()
userConfigRepo = UserConfigRepository()


class PasswordManager:
    def change(self, userId: int, plainTextPassword: str):
        newPasswordHashed = self.hash(plainTextPassword)

        userRepo.updateOne(
            userId,
            dict(
                {
                    "mustChangePassword": False,
                    "password": newPasswordHashed,
                    "passwordChangedAt": datetime.now(timezone.utc),
                }
            ),
        )

    def sync_history(
        self,
        user: dict,
        new_plaintext_password: str,
    ):
        passwordHistories: list[str] = user.get("passwordHistories", [])
        passwordHistoryCount = user.get("passwordHistoryCount", 0)
        new_hashed_password = self.hash(new_plaintext_password)
        #
        #
        # first check if password history is enabled by checking if passwordHistoryCount is greater than 0, else return
        passwordHistoryEnabled = passwordHistoryCount > 0

        if not passwordHistoryEnabled:
            return

        #
        #
        # then check if new password is already in the password history
        # if yes, raise an error
        for password in passwordHistories:
            if self.verify(new_plaintext_password, password) is True:
                # password is already in the history
                raise HTTPException(400, detail="این گذرواژه قبلا استفاده شده است")

        #
        #
        # if no, push the new password to the password history
        # but before pushing, check if the password history is full
        # if yes, remove the oldest password from the password history
        if len(passwordHistories) >= passwordHistoryCount:
            passwordHistories.pop(0)

        # push the new password to the password history
        passwordHistories.append(new_hashed_password)

        # update the user password history
        userRepo.updateOne(
            user.get("id"), dict({"passwordHistories": passwordHistories})
        )

    def hash(self, password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(plain_password, hashed_password)

    def hadExpired(self, user: dict) -> bool:
        global expireDays
        global expireAdvantage

        lastChangeAt: datetime | None = user["passwordChangedAt"]

        if lastChangeAt.tzinfo is None:
            lastChangeAt = lastChangeAt.replace(tzinfo=timezone.utc)

        if user.get("expirePasswordDays", None) != None:
            expireDays = user["expirePasswordDays"]

        else:
            expireDays = userConfigRepo.getExpirePasswordDays()

        if user.get("passwordAdvantageDays", None) != None:
            expireAdvantage = user["passwordAdvantageDays"]

        else:
            expireAdvantage = userConfigRepo.getPasswordAdvantageDays()

        now_utc = datetime.now(timezone.utc)

        dueDate_utc = lastChangeAt + timedelta(days=expireDays + expireAdvantage)

        return now_utc >= dueDate_utc
