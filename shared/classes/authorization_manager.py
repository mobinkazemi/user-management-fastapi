from permissions.repository import PermissionRepository as PR
from rolePermissions.repository import RolePermissionRepository as RPR
from db.redis import redis_client as redis
import json


class AuthorizationManager:
    def __init__(self):
        self.permissionRedisPrekey = "URL_TO_PERMISSIONID_ROLEIDS:"
        self.redis = redis
        self.permissionRepo = PR()
        self.rolePermissionRepo = RPR()

    def permissionRedisSeeder(self):
        prs = self.permissionRepo.findAll()

        for pr in prs:
            # we handle urls like: URL_TO_PERMISSIONID_ROLEIDS:/user/admin/info/{userId}
            if pr["url"].count("/{") > 0:
                # find index of last appearance of "/{" until the end of the string
                # then replace it with "/{dynamicPart}"
                lastIndex = pr["url"].rfind("/{")
                if lastIndex != -1:
                    pr["url"] = pr["url"][:lastIndex] + "/{dynamicPart}"

            key = self.permissionRedisPrekey + pr["url"] + "_" + pr["method"]

            redis.delete(key)

            rolePermissions = self.rolePermissionRepo.findAllAndFilter(
                permission_id=pr["id"]
            )

            roles = []
            for rp in rolePermissions:
                roles.append(rp["role_id"])

            value = [pr["id"], *roles]

            redis.set(key, json.dumps(value))

    def hasAccess(self, url, method, roleIdOfUser, dynamic=False):
        global record

        record = self.redis.get(self.permissionRedisPrekey + url + "_" + method)

        if not record and dynamic:
            # handle dynamic part of the url
            # e.g. /user/admin/info/{userId}
            # we can replace {userId} with any value and check again
            lastIndexOfUrlSlash = url.rfind("/")

            # replace everything after the last slash with {dynamicPart}
            dynamicUrl = url[: lastIndexOfUrlSlash + 1] + "{dynamicPart}"

            print(f"Dynamic URL: {dynamicUrl}")

            # check again with the dynamic url
            record = self.redis.get(
                self.permissionRedisPrekey + dynamicUrl + "_" + method
            )

        if not record:
            print(f"No record found for {url} with method {method}")
            return False

        permissionId, *roleIds = json.loads(record)

        return roleIdOfUser in roleIds
