from roles.repository import RoleRepository as RP
from userRole.repository import UserRoleRepository as URP
from users.repository import UserRepository as UP
from shared.classes.password_manager import PasswordManager as PW
import configparser
from permissions.repository import PermissionRepository as PR
from rolePermissions.repository import RolePermissionRepository as RPR

config = configparser.ConfigParser()

config.read("config.ini")

SUPER_ADMIN_USERNAME = config.get("superadmin", "SUPERADMIN_USERNAME")
SUPER_ADMIN_PASSWORD = config.get("superadmin", "SUPERADMIN_PASSWORD")

passwordManager = PW()
roleRepo = RP()
userRoleRepo = URP()
permissionRepo = PR()
userRepo = UP()
rolePermissionRepo = RPR()


def base_roles_seeder():
    """
    This function seeds the database with base roles.
    """

    # Define the base roles
    roles = [
        {
            "name": "ادمین کل",
            "maxRequestPerMinute": 1000,
            "active": True,
            "workingDayLimit": [0, 1, 2, 3, 4, 5, 6],
            "workingTimeLimit": "00:00-23:59",
        },
        {
            "name": "کاربر",
            "maxRequestPerMinute": 120,
            "active": True,
            "workingDayLimit": [0, 1, 2, 3, 4, 5, 6],
            "workingTimeLimit": "00:00-23:59",
        },
    ]
    for r in roles:
        if roleRepo.findOne(name=r.get("name")):
            continue
        new_role = roleRepo.createOne(r)


def seed_super_admin_user():
    """
    This function seeds the database with a super admin user.
    """
    adminRole = roleRepo.findOne(name="ادمین کل")
    adminRoleId = adminRole.get("id")

    user = userRepo.findByUsername(SUPER_ADMIN_USERNAME)
    if user:
        user_admin_permissions_seeder(user["id"], adminRoleId)
        return

    if not adminRole:
        raise Exception("Admin role not found. Please run base_roles_seeder first.")

    hashed_password = passwordManager.hash(SUPER_ADMIN_PASSWORD)

    new_user = {
        "firstName": SUPER_ADMIN_USERNAME,
        "lastName": SUPER_ADMIN_USERNAME,
        "gender": 1,
        "username": SUPER_ADMIN_USERNAME,
        "password": hashed_password,  # This should be hashed in a real application
        "email": "superamdin@netoran.ir",
        "active": True,
        "twoFAEnabled": False,
        "isSuperAdmin": True,
        "mustChangePassword": False,
    }

    user = userRepo.createOne(new_user)

    adminUserId = user.get("id")

    if userRoleRepo.findOne(userId=adminUserId, roleId=adminRoleId):
        return

    userRole = userRoleRepo.createOne(
        {
            "userId": adminUserId,
            "roleId": adminRoleId,
        }
    )

    userRepo.updateOne(adminUserId, dict({"userRoleId": userRole.get("id")}))

    user_admin_permissions_seeder(user["id"], adminRoleId)


def user_admin_permissions_seeder(userId: int, roleId: int):
    permissions = permissionRepo.findAll()

    for pr in permissions:
        if rolePermissionRepo.findOne(role_id=roleId, permission_id=pr["id"]):
            continue
        rolePermissionRepo.createOne({"role_id": roleId, "permission_id": pr["id"]})
