from seeder.functions.base_roles_seeder import base_roles_seeder, seed_super_admin_user
from seeder.functions.permission_category_seeder import (
    permission_and_permissionCategory_seeder,
)
from seeder.functions.app_config_seeder import user_config_seeder
from shared.classes.authorization_manager import AuthorizationManager as AuthManager


authorize = AuthManager()


def seeder():
    print("\n\n")
    print("seeder is running:")
    base_roles_seeder()
    permission_and_permissionCategory_seeder()
    user_config_seeder()
    seed_super_admin_user()
    authorize.permissionRedisSeeder()
    print("seeder finished.")
