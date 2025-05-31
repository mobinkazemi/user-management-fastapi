from users.model import User
from users.repository import UserRepository
from fastapi import HTTPException
from shared.classes.password_manager import PasswordManager

userRepo = UserRepository()
pm = PasswordManager()


def password_history_manager(
    user: dict, new_plaintext_password: str, new_hashed_password: str
):
    passwordHistories: list[str] = user.get("passwordHistories", [])
    passwordHistoryCount = user.get("passwordHistoryCount", 0)

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
        if pm.verify(new_plaintext_password, password) is True:
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
    userRepo.updateOne(user.get("id"), dict({"passwordHistories": passwordHistories}))
