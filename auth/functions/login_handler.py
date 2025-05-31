from auth.functions.create_token import create_access_token
from users.repository import UserRepository
import datetime
from shared.classes.User_Session_Manager import UserSessionManager as USManager
from userRole.repository import UserRoleRepository
from fastapi import HTTPException

userRepo = UserRepository()
userSessionManager = USManager()
userRoleRepo = UserRoleRepository()


def finalizeLogin(user: dict):
    userRole = userRoleRepo.findById(user["userRoleId"])

    token = create_access_token(
        {
            "id": user["id"],
            "username": user["username"],
            "mustChangePassword": user["mustChangePassword"],
            "roleId": userRole["roleId"],
        }
    )

    del user["password"]
    del user["passwordHistories"]
    del user["passwordHistoryCount"]

    userRepo.updateOne(
        user["id"], {"lastSessionDate": datetime.datetime.now(datetime.timezone.utc)}
    )

    userSessionManager.save(user["id"], token)

    return {"token": token, "user": user}
