from db.redis import redis_client
import configparser
from datetime import datetime, timezone

config = configparser.ConfigParser()
config.read("config.ini")


class UserSessionManager:
    def __init__(self):
        self.sessionPrekey = "USER_LOGGED_IN:"
        self.sessionTTL = config.get("jwt", "JWT_ACCESS_TOKEN_EXPIRE_IN_SECONDS")

    def save(self, userId: int , token: str ):
        key = self.keygen(userId)
        value = str(token)
        redis_client.set(key, value, self.sessionTTL)

    def hasSession(self, userId: int):
        return bool(redis_client.exists(self.keygen(userId)))

    def logout(self, userId: int):
        key = self.keygen(userId)
        redis_client.delete(key)

    def getCurrentSessions(self):
        keys = redis_client.keys(self.sessionPrekey + "*")

        userIds = []

        for key in keys:
            id = key.split(self.sessionPrekey)[1]
            userIds.append(int(id))

        return userIds

    def keygen(self, userId: int):
        return self.sessionPrekey + str(userId)
